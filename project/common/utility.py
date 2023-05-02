import logging
from contextlib import contextmanager
from typing import Iterator

import regex

from project.common.exceptions import NotADimensionError, NotAPriceError

_LOGGER = logging.getLogger(__name__)


def get_quantity(field: str) -> float:
    """Get quantity in grams."""

    field = field.lower()
    field = field.replace(",", ".")
    try:
        if groups := regex.findall(
            r"([0-9]+[.]?[0-9]*)(?:\-)?\s*([mcdkp]?[mlgz])?\s*x\s*([0-9]+[.]?[0-9]*)(?:\-)?\s*([mcdkp]?[mlgz])?",
            field,
            regex.IGNORECASE,
        ):
            return int(groups[0][0]) * _normalize(float(groups[0][2]), groups[0][1] if groups[0][1] else groups[0][3])
        elif groups := regex.findall(r"([0-9]+[.]?[0-9]*)(?:\-)?\s*([mcdkp]?[mlgz])?", field):
            return _normalize(float(groups[0][0]), groups[0][1])
        elif groups := regex.findall(r"(per|al)\s*([mcdkp]?[mlgz]?)", field):
            return _normalize(1.0, groups[0][1])
        else:
            return float(field)
    except (ValueError, NotADimensionError):
        raise NotADimensionError(field)


def get_price(field: str) -> float:
    """Get price in grams."""

    try:
        if groups := regex.findall(r"(-?\d*[,.]\d*)(?:\-)?", field):
            price = groups[0].replace(",", ".")
            if float(price) < 0:
                raise NotAPriceError(f"{field} is not a valid price")
            return float(price)
        if float(field) < 0:
            raise NotAPriceError(f"{field} is not a valid price")
        return float(field)
    except ValueError:
        raise NotAPriceError(field)


def get_id(name: str, supermarket: str) -> str:
    """Get an id per supermarket per product."""

    import hashlib

    # Assumes the default UTF-8
    hash_object = hashlib.md5(f"{name}-{supermarket}".encode())
    return hash_object.hexdigest()


def _normalize(amount: float, unit: str) -> float:
    """Convert everything to grams or L."""

    if unit == "lb":
        return amount * 453.59237
    elif unit == "oz":
        return amount * 28.3495
    elif unit == "kg":
        return amount * 1000
    elif unit in ["ml", "mg"]:
        return amount / 1000
    elif unit in ["cl", "cg"]:
        return amount / 100
    elif unit in ["dl", "dg"]:
        return amount / 10
    elif unit in ["pz", "g", "", "l", "m"]:
        return amount
    raise NotADimensionError(f"{amount} {unit}")


@contextmanager
def log(message: str, emoji: str = "") -> Iterator[None]:
    """Log message with emoji."""

    _LOGGER.info(f"{emoji} {message}")
    yield
    _LOGGER.info(f"✅ Done {message.lower()} {emoji} ")
