import decimal as dec

from beancount.core import amount as bamount
from beancount.core import data as bdata
from hypothesis import strategies as s

from beancount_hypothesis.account import (  # noqa: F401
    AccountGenerator,
    account_name,
)
from beancount_hypothesis.data import (  # noqa: F401
    amount,
    cost,
    costspec,
    decimal,
    inventory,
    position,
)
from beancount_hypothesis.directive import (  # noqa: F401
    balance,
    close,
    commodity,
    custom,
    document,
    event,
    note,
    open,
    pad,
    posting,
    price,
    transaction,
    transactions,
    txnposting,
)

s.register_type_strategy(dec.Decimal, decimal())
s.register_type_strategy(bamount.Amount, amount())
s.register_type_strategy(bdata.Custom, custom())
s.register_type_strategy(bdata.Transaction, transaction())
