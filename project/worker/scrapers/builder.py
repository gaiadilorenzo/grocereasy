from project.common import Supermarket, exceptions
from project.worker.scrapers.base import Scraper
from project.worker.scrapers.coop import CoopScraper
from project.worker.scrapers.lidl import LidlScraper
from project.worker.scrapers.migros import MigrosScraper


def get_scraper(supermarket: str, language: str) -> Scraper:

    match supermarket:
        case Supermarket.LIDL:
            return LidlScraper(language)
        case Supermarket.COOP:
            return CoopScraper(language)
        case Supermarket.MIGROS:
            return MigrosScraper(language)

    raise exceptions.NotSupportedSupermarketError(supermarket)
