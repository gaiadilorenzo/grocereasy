class NotSupportedSupermarketError(Exception):
    """Raised when a supermarket is not found."""

    def __init__(self, supermarket: str):
        super().__init__(f"❌ Supermarket not supported: '{supermarket}'.")


class NotADimensionError(Exception):
    """Raised when the dimension is not recognized."""

    def __init__(self, word: str):
        super().__init__(f"❌{word} is not a dimension.")


class NotAPriceError(Exception):
    """Raised when the price is not recognized."""

    def __init__(self, word: str):
        super().__init__(f"❌{word} is not a price.")
