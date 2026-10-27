from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        raise RuntimeError("Use Balance.get_instance() to access the balance.")

    @classmethod
    def get_instance(cls):
        """Return the shared balance instance."""
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._balance = 0.0
            cls._instance._observers = []
        return cls._instance

    def reset(self):
        """Reset the balance and remove registered observers."""
        self._balance = 0.0
        self._observers.clear()

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, transaction):
        for observer in tuple(self._observers):
            observer.update(self._balance, transaction)

    def add_income(self, amount):
        """Add income to the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.INCOME))

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.EXPENSE))

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self._balance += transaction.amount
        elif transaction.category == TransactionCategory.EXPENSE:
            self._balance -= transaction.amount
        else:
            raise ValueError("Unsupported transaction category.")
        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: ${self._balance:.2f}"
