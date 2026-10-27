import unittest
from unittest.mock import Mock, patch

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import (
    IBalanceObserver,
    LowBalanceAlertObserver,
    PrintObserver,
)


class TestBalanceObservers(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)
        self.observer = Mock(spec=IBalanceObserver)
        self.balance.register_observer(self.observer)

    def test_registered_observer_receives_updated_balance_and_transaction(self):
        transaction = Transaction(100, TransactionCategory.INCOME)
        self.balance.register_observer(self.observer)

        self.balance.apply_transaction(transaction)

        self.observer.update.assert_called_once_with(100, transaction)

    def test_direct_income_and_expense_notify_observers(self):
        self.balance.add_income(100)
        self.observer.update.assert_called_once_with(
            100, Transaction(100, TransactionCategory.INCOME)
        )
        self.observer.reset_mock()

        self.balance.add_expense(40)

        self.observer.update.assert_called_once_with(
            60, Transaction(40, TransactionCategory.EXPENSE)
        )

    def test_unregistered_observer_receives_no_updates(self):
        self.balance.unregister_observer(self.observer)
        self.balance.unregister_observer(self.observer)

        self.balance.add_income(100)

        self.observer.update.assert_not_called()

    def test_invalid_transaction_does_not_notify_observers(self):
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(100, "invalid"))
        self.observer.update.assert_not_called()

    def test_reset_removes_observers(self):
        self.balance.reset()
        self.balance.add_income(100)
        self.observer.update.assert_not_called()

    def test_observer_can_unregister_itself_during_notification(self):
        def unregister(balance, transaction):
            self.balance.unregister_observer(self.observer)

        other_observer = Mock(spec=IBalanceObserver)
        self.balance.register_observer(other_observer)
        self.observer.update.side_effect = unregister

        self.balance.add_income(100)
        self.balance.add_expense(40)

        self.observer.update.assert_called_once_with(
            100, Transaction(100, TransactionCategory.INCOME)
        )
        self.assertEqual(other_observer.update.call_count, 2)
        other_observer.update.assert_any_call(
            100, Transaction(100, TransactionCategory.INCOME)
        )
        other_observer.update.assert_called_with(
            60, Transaction(40, TransactionCategory.EXPENSE)
        )

    @patch("builtins.print")
    def test_print_observer_displays_transaction_and_balance(self, print_mock):
        transaction = Transaction(100, TransactionCategory.INCOME)
        self.balance.register_observer(PrintObserver())

        self.balance.apply_transaction(transaction)

        print_mock.assert_called_once_with(
            f"{transaction} -> Balance: $100.00"
        )


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)
        print_patcher = patch("builtins.print")
        self.print_mock = print_patcher.start()
        self.addCleanup(print_patcher.stop)

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_balance_at_threshold_does_not_trigger_alert(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.add_income(50)

        self.assertFalse(observer.alert_triggered)
        self.print_mock.assert_not_called()

    def test_alert_is_printed_once_until_balance_recovers(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.add_income(40)
        self.balance.add_expense(10)
        self.print_mock.assert_called_once_with("Low balance alert: $40.00")

        self.balance.add_income(20)
        self.assertFalse(observer.alert_triggered)
        self.print_mock.reset_mock()
        self.balance.add_expense(1)

        self.assertTrue(observer.alert_triggered)
        self.print_mock.assert_called_once_with("Low balance alert: $49.00")


if __name__ == "__main__":
    unittest.main()
