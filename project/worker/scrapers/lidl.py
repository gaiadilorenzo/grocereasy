import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List

import requests
from bs4 import BeautifulSoup

from project.common import Item, Supermarket, utility
from project.worker.scrapers.base import Scraper

_MAX = 10000
_LOGGER = logging.getLogger(__name__)


class LidlScraper(Scraper):
    """Lidl scraper."""

    def __init__(self, language: str):
        super().__init__(language)

    def _get_items_per_category(self, url: str, *, limit: int | None = None) -> List[Item]:

        _LOGGER.info(f"💁🏻‍♀️ Fetching {url}")
        page = self.get(url, requests)

        items = BeautifulSoup(page.content, "html.parser").find_all(
            "div", class_="product details product-item-details"
        )

        with ThreadPoolExecutor(max_workers=max(len(items), 1)) as executor:
            products = [executor.submit(self._get_item, url, j, item).result() for j, item in enumerate(items[:limit])]

        _LOGGER.info(f"✅ Done fetching {url} / {len(products)} ")
        return [product for product in products if product is not None]

    def _get_item(self, url: str, rank: int, item: Any) -> Item | None:
        try:
            name = item.find("strong", class_="product name product-item-name").text
            price = utility.get_price(item.find("strong", class_="pricefield__price")["content"])
            item_link = item.find("a", class_="product-item-link")["href"]
            product = url.split("=")[-1]
            page = self.get(item_link, requests)
            product_page = BeautifulSoup(page.content, "html.parser")
            quantity = utility.get_quantity(product_page.find("span", class_="pricefield__footer").text)
            brand = brand.text if (brand := product_page.find("p", class_="brand-name")) else None
            offer = offer.text if (offer := product_page.find("span", class_="pricefield__header")) else None
            description = (
                description.text
                if (description := product_page.find("div", class_="product attribute overview"))
                else None
            )

            return Item(
                product=product,
                brand=brand if brand else Supermarket.LIDL,
                name=name,
                id=utility.get_id(name=item_link, supermarket=Supermarket.LIDL),
                price=price,
                quantity=quantity,
                supermarket=Supermarket.LIDL,
                link=f"{item_link}",
                rank=rank,
                offer=offer,
                description=description,
            )

        except Exception as e:
            _LOGGER.exception(f"🚩 Caught exception while fetching item: {url} ({e})")
            return None
