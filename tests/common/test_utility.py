import pytest

from project.common.exceptions import NotAPriceError
from project.common.utility import get_price, get_quantity


@pytest.mark.parametrize(
    "field, expected_output",
    [("$10.99", 10.99), ("10.99 CHF", 10.99), ("10,99", 10.99), ("10.99", 10.99), ("10", 10.0), ("'5.-", 5.0)],
)
def test_valid_price(field, expected_output):
    assert get_price(field) == expected_output


@pytest.mark.parametrize(
    "input_field",
    [
        "invalid",
        "-10.99",
        "not a price",
    ],
)
def test_invalid_price(input_field):
    with pytest.raises(NotAPriceError):
        get_price(input_field)


@pytest.mark.parametrize(
    "input_field, expected_output",
    [
        ("100g", 100.0),
        ("100 g", 100.0),
        ("per kg", 1000.0),
        ("100g x 5", 500.0),
        ("100 g x 5", 500.0),
        ("100", 100.0),
        ("12 pz", 12.0),
        ("10 x 5g", 50.0),
    ],
)
def test_get_quantity(input_field, expected_output):
    output = get_quantity(input_field)
    assert output == expected_output
