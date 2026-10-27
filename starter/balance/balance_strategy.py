from abc import ABC, abstractmethod


class BalanceStrategy(ABC):
    @abstractmethod
    def calculate(self, balance, amount):
        """Return the balance after applying an amount."""
        raise NotImplementedError


class IncomeStrategy(BalanceStrategy):
    def calculate(self, balance, amount):
        return balance + amount


class ExpenseStrategy(BalanceStrategy):
    def calculate(self, balance, amount):
        return balance - amount
