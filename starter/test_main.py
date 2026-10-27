import unittest
from contextlib import redirect_stdout
from io import StringIO

from balance.balance import Balance
from main import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)

    def test_main_applies_transactions_and_can_run_again(self):
        outputs = []
        for _ in range(2):
            output = StringIO()
            with redirect_stdout(output):
                main()
            outputs.append(output.getvalue())
            self.assertEqual(self.balance.get_balance(), 1375)

        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0].count("Low balance alert:"), 1)
        self.assertTrue(outputs[0].endswith("Net balance: $1375.00\n"))


if __name__ == "__main__":
    unittest.main()
