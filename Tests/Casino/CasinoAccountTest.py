import unittest

from Application.Casino.CasinoAccount import CasinoAccount


class CasinoAccountTest(unittest.TestCase):

    def setUp(self):
        self.account = CasinoAccount("test_user", "test_password", 0.00)

    def test_constructor_no_balance(self):
        self.assertEqual(self.account.username, "test_user")
        self.assertEqual(self.account.password, "test_password")
        self.assertEqual(self.account.balance, 0.00)

    def test_constructor_with_balance(self):
        account = CasinoAccount("test_account", "test_password", 25.85)
        self.assertEqual(account.username, "test_account")
        self.assertEqual(account.password, "test_password")
        self.assertEqual(account.balance, 25.85)

    def test_balance_setter(self):
        self.account.balance = 25.99
        self.assertEqual(self.account.balance, 25.99)

    def test_balance_setter_negative(self):
        with self.assertRaises(ValueError):
            self.account.balance = -25

    def test_add_winnings(self):
        expected = self.account.balance + 25
        actual = self.account.add_winnings(25)
        self.assertEqual(expected, actual)

    def test_add_winnings_negative(self):
        with self.assertRaises(ValueError):
            self.account.add_winnings(-1)