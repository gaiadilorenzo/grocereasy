import pytest

from project.common import Item
from project.worker.scrapers.lidl import LidlScraper


@pytest.mark.vcr()  # TODO: make test connectionless
@pytest.mark.parametrize("url", [("https://sortiment.lidl.ch/it/catalogsearch/result/?q=pollo")])
def test__get_items_per_category(url: str) -> None:
    lidl_scraper = LidlScraper()
    items = lidl_scraper._get_items_per_category(url, limit=9)
    assert len(items) > 0
    assert type(items[0]) == Item
