import abc
import contextlib
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import requests
import selenium
import tenacity
import urllib3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from project.common import Item

_LOGGER = logging.getLogger(__name__)


class Scraper(abc.ABC):
    URL: str

    def __init__(self, language: str) -> None:
        super().__init__()
        self._language = language

    def get_items(self, urls: list[str]) -> list[Item]:  # noqa: D102 (to inherit docstring from base class)
        """Get all items."""

        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            futures = executor.map(self._get_items_per_category, urls)

        items = [product for future in futures for product in future]
        return items

    def _get_items_per_category(
        self, url: str, *, limit: int | None = None
    ):  # noqa: D102 (to inherit docstring from base class)
        """Get items per category."""

    @contextlib.contextmanager
    def session(self):
        """Open a session."""
        try:
            options = webdriver.ChromeOptions()

            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("start-maximized")
            options.add_argument("disable-infobars")
            options.add_argument("--disable-extensions")

            browser = webdriver.Chrome(options=options)
            browser.set_page_load_timeout(60)
            yield browser
        except Exception as e:
            _LOGGER.error(f"🚨 {e}")
            browser.quit()

    @tenacity.retry(
        reraise=True,
        retry=tenacity.retry_if_exception_type(
            (
                selenium.common.exceptions.TimeoutException,
                requests.exceptions.ConnectionError,
                urllib3.exceptions.ProtocolError,
            )
        ),
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_random_exponential(multiplier=1, max=60),
    )
    def get(self, url: str, session: Any) -> Any:
        """Get the page source."""

        return session.get(url)

    @tenacity.retry(
        reraise=True,
        retry=tenacity.retry_if_exception_type(
            (
                selenium.common.exceptions.TimeoutException,
                requests.exceptions.ConnectionError,
                urllib3.exceptions.ProtocolError,
            )
        ),
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_random_exponential(multiplier=1, max=60),
    )
    def wait(self, browser, until):
        """Wait for an element to be present."""

        wait = WebDriverWait(browser, timeout=60)
        wait.until(until)
        return wait
