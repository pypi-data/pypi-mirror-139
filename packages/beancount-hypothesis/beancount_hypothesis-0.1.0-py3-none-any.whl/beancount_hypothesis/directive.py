import decimal
import random
from typing import Any, TypeVar

from beancount.core import amount, data
from hypothesis import strategies as s

from beancount_hypothesis import account, common

T = TypeVar("T", bound="data.Directive")


def directive(ty: type[T], **kwargs) -> s.SearchStrategy[T]:
    """Generates the given directive type.

    Args:
        ty: The type of directive to generate

    Returns:
        A new instance of the generated directive
    """
    return s.builds(ty, meta=meta(), **kwargs)


@s.composite
def meta(draw: s.DrawFn) -> dict[str, Any]:
    """Generates metadata for directives.

    Returns:
        A new search strategy
    """
    filename = draw(common.filename())
    lineno = random.randrange(1, 100000)

    return {"filename": filename, "lineno": lineno}


def balance() -> s.SearchStrategy[data.Balance]:
    """Generate a Balance directive.

    Returns:
        A new search strategy
    """
    return directive(data.Balance, account=account.account_name())


def close() -> s.SearchStrategy[data.Close]:
    """Generate a Close directive.

    Returns:
        A new search strategy
    """
    return directive(data.Close, account=account.account_name())


def commodity(
    currencies: list[str] = None,
) -> s.SearchStrategy[data.Commodity]:
    """Generate a Commodity directive.

    Returns:
        A new search strategy
    """
    return directive(data.Commodity, currency=common.currency(currencies))


def custom() -> s.SearchStrategy[data.Custom]:
    """Generate a Custom directive.

    Returns:
        A new search strategy
    """
    return directive(data.Custom, values=s.lists(common.word()))


def document() -> s.SearchStrategy[data.Document]:
    """Generate a Document directive.

    Returns:
        A new search strategy
    """
    return directive(data.Document, filename=common.filename())


def event() -> s.SearchStrategy[data.Event]:
    """Generate an Event directive.

    Returns:
        A new search strategy
    """
    return directive(data.Event)


def note() -> s.SearchStrategy[data.Note]:
    """Generate a Note directive.

    Returns:
        A new search strategy
    """
    return directive(data.Note, account=account.account_name())


def open(currencies: list[str] = None) -> s.SearchStrategy[data.Open]:
    """Generate an Open directive.

    Returns:
        A new search strategy
    """
    return directive(
        data.Open,
        account=account.account_name(),
        currencies=s.lists(
            common.currency(currencies), min_size=2, max_size=5
        ),
    )


def pad() -> s.SearchStrategy[data.Pad]:
    """Generate a Pad directive.

    Returns:
        A new search strategy
    """
    return directive(
        data.Pad,
        account=account.account_name(),
        source_account=account.account_name(),
    )


def posting() -> s.SearchStrategy[data.Posting]:
    """Generate a Posting.

    Returns:
        A new search strategy
    """
    return s.builds(data.Posting, meta=meta())


def price(currencies: list[str] = None) -> s.SearchStrategy[data.Price]:
    """Generate a Posting.

    Returns:
        A new search strategy
    """
    return directive(data.Price, currency=common.currency(currencies))


@s.composite
def transaction(draw: s.DrawFn) -> data.Transaction:
    """Generates a random transaction

    Returns:
        A new search strategy
    """
    ag = account.AccountGenerator()
    accts = ag.generate()
    return draw(_transaction_with_accounts(accts=accts))


@s.composite
def transactions(draw: s.DrawFn, min=3, max=5) -> list[data.Transaction]:
    """Generates a list of transactions.

    Args:
        min: The minimum number to generate
        max: The maximum number to generate

    Returns:
        A new search strategy
    """
    ag = account.AccountGenerator()
    accts = ag.generate()
    return draw(
        s.lists(
            _transaction_with_accounts(accts=accts), min_size=min, max_size=max
        )
    )


def txnposting() -> s.SearchStrategy[data.TxnPosting]:
    """Generates a TxnPosting.

    Returns:
        A new search strategy
    """
    return s.builds(data.TxnPosting, txn=transaction(), posting=posting())


@s.composite
def _transaction_with_accounts(
    draw: s.DrawFn,
    accts: list[str],
    currency="USD",
    postings_min=2,
    postings_max=5,
) -> data.Transaction:
    """Generates a random transaction.

    The generated transaction will contain a random number of postings that may
    not have unique amounts but will always sum to zero. The accounts used in
    each posting will be unique and will be randomly pulled from the given list
    of account names.

    Args:
        accts: A list of account names to pull from for generating postings
        currency: The currency to use in postings
        postings_min: The minimum number of postings to generate
        postings_max: The maximum number of postings to generate

    Returns:
        A new search strategy
    """
    postings = []

    numbers = draw(
        s.lists(
            s.decimals(
                min_value=-50,
                max_value=50,
                allow_infinity=False,
                allow_nan=False,
            ).filter(lambda n: n > 1 or n < -1),
            min_size=postings_min,
            max_size=postings_max,
        )
    )

    numbers.append(decimal.Decimal(-sum(numbers)))
    assert sum(numbers) == 0

    amts = [amount.Amount(number=n, currency=currency) for n in numbers]
    used_accounts = []
    for amt in amts:
        account = draw(
            s.sampled_from(accts).filter(lambda a: a not in used_accounts)
        )
        used_accounts.append(account)

        postings.append(
            data.Posting(
                account=account,
                units=amt,
                cost=None,
                price=None,
                flag=None,
                meta=None,
            )
        )

    txn = data.Transaction(
        meta=draw(meta()),
        date=draw(s.dates()),
        flag="*",
        payee=None,
        narration=draw(common.words()),
        tags=None,
        links=None,
        postings=postings,
    )

    return txn
