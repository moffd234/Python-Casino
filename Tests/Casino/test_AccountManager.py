import unittest
from unittest.mock import patch, mock_open

from Application.Casino.Accounts.AccountManager import AccountManager, write_new_account_to_csv
from Application.Casino.Accounts.CasinoAccount import CasinoAccount


class AccountManagerTest(unittest.TestCase):

    @patch("Application.Casino.AccountManager.read_from_csv", return_value=[])
    def setUp(self, mock_read_from_csv):
        self.manager: AccountManager = AccountManager()

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

    def test_get_account(self):
        expected: CasinoAccount = CasinoAccount("test_user", "secure123")

        self.manager.accounts.append(expected)
        actual: CasinoAccount = self.manager.get_account("test_user", "secure123")

        self.assertEqual(expected, actual)

    def test_get_account_none(self):

        actual: CasinoAccount = self.manager.get_account("this_name_won't_be_used", "secure123")

        self.assertIsNone(actual)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="user1,pass1,500\nuser2,pass2,1000\n")
    def test_read_from_csv(self, mock_file, mock_exists):
        manager = AccountManager()
        manager = AccountManager()

        user_one = manager.accounts[0]
        user_two = manager.accounts[1]

        self.assertEqual(len(manager.accounts), 2)
        self.assertEqual(user_one.username, "user1")
        self.assertEqual(user_two.username, "user2")
        self.assertEqual(user_one.password, "pass1")
        self.assertEqual(user_two.password, "pass2")
        self.assertEqual(user_one.balance, 500)
        self.assertEqual(user_two.balance, 1000)
