import unittest
from Application.Casino.AccountManager import AccountManager
from Application.Casino.CasinoAccount import CasinoAccount


class AccountManagerTest(unittest.TestCase):

    def setUp(self):
        self.manager: AccountManager = AccountManager()

    def test_create_account(self):
        subject = self.manager.create_account("username", "password")

        expected_username = "username"
        expected_password = "password"
        expected_balance = 0.0

        actual_username = subject.username
        actual_password = subject.password
        actual_balance = subject.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)

    def test_create_account_username_exist(self):
        self.manager.accounts.append(CasinoAccount("username", "password"))
        subject = self.manager.create_account("username", "password")

        self.assertIsNone(subject)