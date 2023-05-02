import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from project.common import Item, Supermarket, utility
from project.worker.scrapers.base import Scraper

_LOGGER = logging.getLogger(__name__)

_NEXT_PAGE = {
    "it": "Visualizza altri",
    "en": "See next",
    "de": "weitere ansehen",
}


class MigrosScraper(Scraper):
    """Migros scraper."""

    URL = "https://www.migros.ch"

    def __init__(self, language: str):
        super().__init__(language)

    def _get_items_per_category(self, url: str, *, limit: int | None = None) -> List[Item]:

        _LOGGER.info(f"💁🏻‍♀️ Fetching {url}")

        with self.session() as browser:
            products = []
            self.get(url, browser)
            self.wait(browser, EC.presence_of_element_located((By.CLASS_NAME, "product-show-details")))

            buttons = browser.find_elements(by=By.CSS_SELECTOR, value="button")
            flag = [new_button for new_button in buttons if "Visualizza altri" in new_button.text]

            while flag:  # TODO: find a cleaner way to do this
                for button in buttons:
                    if _NEXT_PAGE[self._language] in button.text:
                        button.click()
                        time.sleep(2)

                buttons = browser.find_elements(by=By.CSS_SELECTOR, value="button")
                flag = [new_button for new_button in buttons if "Visualizza altri" in new_button.text]

            items = BeautifulSoup(browser.page_source, "html.parser").find_all("a", class_="product-show-details")

            with ThreadPoolExecutor(max_workers=max(len(items), 1)) as executor:
                products = [
                    executor.submit(self._get_item, url, browser, j, item).result()
                    for j, item in enumerate(items[:limit])
                ]

        _LOGGER.info(f"✅ Done fetching {url} / {len(products)} ")
        return [product for product in products if product is not None]

    def _get_item(self, url: str, browser: Any, rank: int, item: Any) -> Item | None:
        try:
            item_link = item["href"]
            product = url.split("=")[-1]

            self.get(f"{self.URL}{item_link}", browser)
            self.wait(browser, EC.presence_of_element_located((By.CLASS_NAME, "product-core-container")))

            product_page = BeautifulSoup(browser.page_source, "html.parser")

            name = product_page.find("h1", class_="ng-star-inserted").text
            name = name.replace("\n", "")
            quantity = utility.get_quantity(product_page.find("span", class_="weight-priceUnit").text)
            price = utility.get_price(item.find("span", class_="actual").text)
            brands = product_page.find_all("mo-product-detail-brand-label")
            brand = " ".join([brand.find("img")["alt"] for brand in brands])

            if offer := product_page.find("span", class_="product-badge badge-promo"):
                offer = offer.text

            return Item(
                product=product,
                brand=brand if brand else Supermarket.MIGROS,
                name=name,
                id=utility.get_id(name=f"{self.URL}{item_link}", supermarket=Supermarket.MIGROS),
                price=price,
                quantity=quantity,
                supermarket=Supermarket.MIGROS,
                link=f"{self.URL}{item_link}",
                rank=rank,
                offer=offer,
            )
        except Exception as e:
            _LOGGER.exception(f"🚩 Caught exception while fetching item: {url} ({e})")
            return None
