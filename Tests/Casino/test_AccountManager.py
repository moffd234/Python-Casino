from Tests.BaseTest import BaseTest
from unittest.mock import patch, mock_open, MagicMock

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.CasinoAccount import CasinoAccount
from Application.Casino.Accounts.UserAccount import UserAccount


class AccountManagerTest(BaseTest):

    def setUp(self):
        super().setUp()

    def test_create_account(self):
        subject = self.manager.create_account("username", "password")

        expected_username = "username"
        expected_password = "password"
        expected_balance = 50.0

        actual_username = subject.username
        actual_password = subject.password
        actual_balance = subject.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)

    def test_create_account_username_exist(self):
        self.manager.create_account("test_username", "test_password")
        subject = self.manager.create_account("test_username", "test_password")

        self.assertIsNone(subject)

    def test_get_account(self):
        self.manager.create_account("test_username", "test_password")
        expected = UserAccount("test_username", "test_password", 50.0)
        actual = self.manager.get_account("test_username", "test_password")

        self.assertEqual(expected.username, actual.username)
        self.assertEqual(expected.password, actual.password)
        self.assertEqual(expected.balance, actual.balance)

    def test_get_account_none(self):

        actual: CasinoAccount = self.manager.get_account("this_name_won't_be_used", "secure123")

        self.assertIsNone(actual)
