import logging

from project.common import Product
from project.orchestrator.url_providers.base import URLProvider

_LOGGER = logging.getLogger(__name__)


class MigrosURLProvider(URLProvider):
    """CarrefourScraper URL provider."""

    _URL = "https://www.migros.ch"

    def __init__(self, language: str):
        super().__init__()
        self._url = f"{self._URL}/{language}"

    def get_urls(
        self, products: list[str] = Product.values
    ) -> list[str]:  # noqa: D102 (to inherit docstring from base class)
        return [f"{self._url}/search?query={url}" for url in products]

    def get_supermarket(self) -> str:
        return "Migros"
