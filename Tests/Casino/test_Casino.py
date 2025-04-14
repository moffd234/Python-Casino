from unittest.mock import patch, call

from Application.Casino.Casino import *
from Tests.BaseTest import BaseTest


class test_Casino(BaseTest):

    def setUp(self):
        super().setUp()
        self.casino = Casino()
        self.casino.account = self.manager.create_account("username", "password")

    def test_print_welcome(self):
        expected: str = r"""[34m
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888 
        """
        actual: str = self.casino.print_welcome()
        self.assertEqual(expected.strip(), actual.strip())

    def assert_account_info(self, account):
        expected_username = "test_username"
        expected_password = "test_password"
        expected_balance = 50.0
        actual_username = account.username
        actual_password = account.password
        actual_balance = account.balance
        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)


    @patch("Application.Casino.Accounts.AccountManager.AccountManager.get_account",
           return_value=UserAccount("test_username", "test_password", 50.0))
    @patch("Application.Utils.IOConsole.IOConsole.get_string_input", side_effect=["test_username", "test_password"])
    def test_handle_login(self, mock_inputs, mock_get_account):
        account: UserAccount = self.casino.handle_login()

        self.assert_account_info(account)

    @patch("Application.Casino.Accounts.AccountManager.AccountManager.get_account", return_value=None)
    @patch("Application.Utils.IOConsole.IOConsole.get_string_input", side_effect=["wrong_user", "wrong_pass"] * 5)
    def test_handle_login_fail(self, mock_get_string_input, mock_get_account):
        account = self.casino.handle_login()
        self.assertIsNone(account)

    @patch("Application.Casino.Accounts.AccountManager.AccountManager.create_account",
           return_value=UserAccount("test_username", "test_password", 50.0))
    @patch("Application.Utils.IOConsole.IOConsole.get_string_input", side_effect=["test_username", "test_password"])
    def test_handle_signup(self, mock_inputs, mock_get_account):
        account: UserAccount = self.casino.handle_signup()

        self.assert_account_info(account)

    @patch("builtins.print")
    @patch("builtins.input", return_value="50")
    def test_handle_add_funds(self, mock_input, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()

        actual_balance: float = self.casino.account.balance

        mock_print.assert_called_once_with(f"{ANSI_COLORS.GREEN.value}You have added $50.0 to your funds!"
                                           f" New Balance is {self.casino.account.balance}")
        self.assertEqual(expected_balance, actual_balance)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["-1", "50"])
    def test_handle_add_funds_negative(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=[".001", "50"])
    def test_handle_add_funds_low_decimal(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1000", "50"])
    def test_handle_add_funds_1000(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    def add_funds_and_assert(self, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()
        actual_balance: float = self.casino.account.balance
        mock_print.assert_has_calls([
            call(self.casino.console.print_colored("Invalid input. Please try again", ANSI_COLORS.RED)),
            call(
                f"{ANSI_COLORS.GREEN.value}You have added $50.0 to your funds! New Balance is {self.casino.account.balance}")
        ])
        self.assertEqual(expected_balance, actual_balance)