import unittest
from unittest.mock import patch, mock_open

from Application.Casino.AccountManager import AccountManager, write_new_account_to_csv
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

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_write_new_account_to_csv(self, mock_csv_writer, mock_file):
        test_account = CasinoAccount("test_user", "secure123", 500)
        write_new_account_to_csv(test_account)

        mock_file.assert_called_once_with("./accounts.csv", "a", newline='')
        mock_csv_writer.return_value.writerow.assert_called_once_with(["test_user", "secure123", 500])



