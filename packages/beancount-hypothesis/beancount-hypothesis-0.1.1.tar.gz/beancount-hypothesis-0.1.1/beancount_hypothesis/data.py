import decimal as dec

from beancount.core import amount as amt
from beancount.core import inventory as inv
from beancount.core import position as pos
from hypothesis import strategies as s

from beancount_hypothesis import common


def decimal() -> s.SearchStrategy[dec.Decimal]:
    """Generates a random decimal value.

    Returns:
        A new search strategy.
    """
    return s.decimals(
        min_value=1, max_value=100, allow_infinity=False, allow_nan=False
    ).filter(lambda d: d is not None)


def amount(currencies: list[str] = ["USD"]) -> s.SearchStrategy[amt.Amount]:
    """Generates a random Amount.

    Args:
        currencies: An optional list of currencies to select from.

    Returns:
        A new search strategy.
    """
    return s.builds(
        amt.Amount,
        number=decimal(),
        currency=common.currency(currencies),
    )


def cost(currencies: list[str] = ["USD"]) -> s.SearchStrategy[pos.Cost]:
    """Generates a random Cost.

    Args:
        currencies: An optional list of currencies to select from.

    Returns:
        A new search strategy.
    """
    return s.builds(pos.Cost, currency=common.currency(currencies))


def costspec(
    currencies: list[str] = ["USD"],
) -> s.SearchStrategy[pos.CostSpec]:
    """Generates a random CostSpec.

    Args:
        currencies: An optional list of currencies to select from.

    Returns:
        A new search strategy.
    """
    return s.builds(pos.CostSpec, currency=common.currency(currencies))


@s.composite
def inventory(draw: s.DrawFn) -> inv.Inventory:
    """Generates a random Inventory of Positions.

    Returns:
        A new search strategy.
    """
    positions = draw(s.lists(position(), max_size=3))
    return inv.Inventory(positions)


def position() -> s.SearchStrategy[pos.Position]:
    """Generates a random Position.

    Returns:
        A new search strategy.
    """
    return s.builds(pos.Position)
