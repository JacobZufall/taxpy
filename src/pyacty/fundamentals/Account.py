"""
Account.py

The justification for this class is to reduce the amount of for loops used in other files to improve readability. Prior
to this class, dictionaries were used, which required nested loops often, which got annoying. The ability to access
an attribute directly reduces the amount of for loops needed.
"""

from typing import override

from .Money import Money
from ..constants import BAL_TYPES


class Account:
    def __init__(self, name: str, normal_balance: str, balance: int | float | Money, contra: bool = False,
                 term: str | None = None) -> None:
        # Ensures normal_balance is either "debit" or "credit".
        if normal_balance.lower() not in BAL_TYPES:
            raise ValueError

        self.name: str = name
        self.normal_balance: str = normal_balance.lower()
        self.balance: Money = balance if isinstance(balance, Money) else Money(balance)
        self.contra: bool = contra
        self.term: str | None = term

    # Dunders
    @override
    def __str__(self) -> str:
        return (f"{self.name}:\n"
                f"    Normal balance: {self.normal_balance}\n"
                f"    Term: {self.term}\n"
                f"    Balance: {self.balance}")

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"

    # TODO: When performing arithmatic on this class, should a new account be returned that has all the properties of
    #  the account on the left side of the operation (with the new balance)? Or, should it just return the new balance?

    # Properties
    @property
    def true_balance(self) -> Money:
        multiplier: int = 1

        if (self.normal_balance == "debit" and self.contra) or self.normal_balance == "credit":
            multiplier = -1

        return self.balance * multiplier