import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List

import requests
from bs4 import BeautifulSoup

from project.common import Item, Supermarket, utility
from project.worker.scrapers.base import Scraper

_LOGGER = logging.getLogger(__name__)

_NO_ELEMENT = {"it": "Ops, questo contenuto non è disponibile."}


class CoopScraper(Scraper):
    """Coop scraper."""

    URL = "https://www.coop.ch"

    def __init__(self, language: str):
        super().__init__(language)

    def _get_items_per_category(self, url: str, *, limit: int | None = None) -> List[Item]:

        with self.session() as browser:
            products = []
            for i in range(1, 5):  # TODO: find a way to get the number of pages

                self.get(f"{url}&page={i}", browser)
                page_source = browser.page_source

                if _NO_ELEMENT[self._language] in [
                    h1.text for h1 in BeautifulSoup(page_source, "html.parser").find_all("h1")
                ]:
                    return []

                items = BeautifulSoup(page_source, "html.parser").find_all(
                    "div", class_="productTile__wrapper productTile__wrapper--noEqualHeights"
                )
                print(items)
                _LOGGER.info(f"💁🏻‍♀️ Fetching {url}&page={i}")

                with ThreadPoolExecutor(max_workers=max(len(items), 1)) as executor:
                    products += [
                        executor.submit(self._get_item, url, i * j, item).result()
                        for j, item in enumerate(items[:limit])
                    ]

                _LOGGER.info(f"✅ Done fetching {url}&page={i} / {len(products)} ")

        return [product for product in products if product is not None]

    def _get_item(self, url: str, rank: int, item: Any) -> Item | None:
        try:

            item_link = item.find("a", class_="productTile")["href"]
            product = url.split("=")[-1]
            page = self.get(f"{self.URL}{item_link}", requests)
            product_page = BeautifulSoup(page.content, "html.parser")
            name = product_page.find("h1", class_="title title--productBasicInfo").text
            name = name.replace("\n", "")
            quantity = utility.get_quantity(product_page.find("span", class_="productBasicInfo__quantity-text").text)
            price = utility.get_price(item.find("p", class_="productTile__price-value-lead-price").text)
            brand = product_page.find("span", class_="productBasicInfo__productMeta-value-item").text
            offer = (
                offer.text
                if (offer := product_page.find("span", class_="productBasicInfo__price-text-saving-inner"))
                else None
            )

            return Item(
                product=product,
                brand=brand if brand else Supermarket.COOP,
                name=name,
                id=utility.get_id(name=item_link, supermarket=Supermarket.COOP),
                price=price,
                quantity=quantity,
                supermarket=Supermarket.COOP,
                link=f"{self.URL}{item_link}",
                rank=rank,
                offer=offer,
            )

        except Exception as e:  # TODO: find a better way to intercept errors
            _LOGGER.exception(f"🚩 Caught exception while fetching item: {url} ({e})")
            return None
