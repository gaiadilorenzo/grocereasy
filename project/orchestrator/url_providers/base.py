import abc


class URLProvider(abc.ABC):
    """Base class for URL providers."""

    def __init__(self):
        """Initialize the URL provider."""

    @abc.abstractmethod
    def get_urls(self, products: list[str] = []) -> list[str]:
        """Return the list of urls to fetch for a supermarket."""

    @abc.abstractmethod
    def get_supermarket(self) -> str:
        """Return the supermarket."""
