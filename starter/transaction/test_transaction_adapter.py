import unittest

from balance.balance import Balance
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapted_income_updates_balance_when_applied(self):
        balance = Balance.get_instance()
        balance.reset()
        self.addCleanup(balance.reset)
        balance.add_income(100)
        external_income = ExternalFreelanceIncome(
            125.75, "INV-12346", "Bug fixes"
        )

        transaction = TransactionAdapter(external_income).to_transaction()

        self.assertEqual(balance.get_balance(), 100)
        balance.apply_transaction(transaction)
        self.assertEqual(balance.get_balance(), 225.75)


if __name__ == "__main__":
    unittest.main()
