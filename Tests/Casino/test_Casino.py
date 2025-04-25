from unittest.mock import patch, call

from Application.Casino.Casino import *
from Tests.BaseTest import BaseTest


class TestCasino(BaseTest):

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

    @patch("Application.Casino.Accounts.AccountManager.AccountManager.create_account",
           side_effect=[None, UserAccount("test_username", "test_password", 50.0)])
    @patch("Application.Utils.IOConsole.IOConsole.get_string_input",
           side_effect=["test_username", "test_password"] * 2)
    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    def test_handle_signup_account_exist(self, mock_print, mock_inputs, mock_create_account):
        account: UserAccount = self.casino.handle_signup()

        mock_print.assert_called_once_with("Account with that username already exists")
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
    @patch("builtins.input", side_effect=[".99", "50"])
    def test_handle_add_funds_low_decimal(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    def add_funds_and_assert(self, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()
        actual_balance: float = self.casino.account.balance
        mock_print.assert_has_calls([
            call(self.casino.console.print_colored("Please enter a valid amount "
                                                   "(A positive number >= 1.00 with no more than 2 decimal places).",
                                                   ANSI_COLORS.RED)),
            call(
                f"{ANSI_COLORS.GREEN.value}You have added $50.0 to your funds! New Balance is {self.casino.account.balance}")
        ])
        self.assertEqual(expected_balance, actual_balance)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["password", "new_password"])
    def test_reset_password(self, mock_input, mock_print):
        self.casino.reset_password()

        expected_password = "new_password"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with(self.casino.console.print_colored(f"Your password has been updated!", ANSI_COLORS.GREEN))
        self.assertEqual(expected_password, actual_password)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["test_pAsSwOrD123!", "new_password"])
    def test_reset_password_case_sensitive(self, mock_input, mock_print):
        account: UserAccount = self.casino.manager.create_account("test_username", "test_pAsSwOrD123!")
        self.casino.account = account
        self.casino.reset_password()

        expected_password = "new_password"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with(
            self.casino.console.print_colored(f"Your password has been updated!", ANSI_COLORS.GREEN))
        self.assertEqual(expected_password, actual_password)

    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    @patch("builtins.input", side_effect=["wrong_password"] * 5)
    def test_reset_password_failed_times(self, mock_input, mock_print_error):
        expected_password: str = self.casino.account.password
        self.casino.reset_password()

        actual_password = self.casino.account.password

        # 5 incorrect password messages and 1 lockout message
        mock_print_error.assert_has_calls([
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Too many invalid attempts. Please try again")
        ])
        self.assertEqual(expected_password, actual_password)

    @patch("builtins.print")
    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    @patch("builtins.input", side_effect=["wrong_password", "wrong_password", "password", "new_password"])
    def test_reset_password_failed_then_works(self, mock_input,mock_print_error, mock_print):
        self.casino.reset_password()

        expected_password: str = "new_password"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with((self.casino.console.print_colored("Your password has been updated!",
                                                                              ANSI_COLORS.GREEN)))
        mock_print_error.assert_has_calls([
            call("Passwords do not match"),
            call("Passwords do not match")
        ])
        self.assertEqual(expected_password, actual_password)

    @patch("Application.Casino.Casino.Casino.add_funds")
    @patch("builtins.input", return_value="add")
    def test_handle_manage_selection_add(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch("Application.Casino.Casino.Casino.add_funds")
    @patch("builtins.input", return_value="add-funds")
    def test_handle_manage_selection_add_dash_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch("Application.Casino.Casino.Casino.add_funds")
    @patch("builtins.input", return_value="add funds")
    def test_handle_manage_selection_add_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch("Application.Casino.Casino.Casino.reset_password")
    @patch("builtins.input", return_value="reset")
    def test_handle_manage_selection_reset(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch("Application.Casino.Casino.Casino.reset_password")
    @patch("builtins.input", return_value="reset password")
    def test_handle_manage_selection_reset_password(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch("Application.Casino.Casino.Casino.reset_password")
    @patch("builtins.input", return_value="reset-password")
    def test_handle_manage_selection_reset_dash_password(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch("builtins.input", return_value="back")
    def test_handle_manage_selection_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch("builtins.input", return_value="go back")
    def test_handle_manage_selection_go_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch("builtins.input", return_value="go-back")
    def test_handle_manage_selection_go_dash_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch("builtins.print")
    @patch("Application.Casino.Casino.Casino.add_funds")
    @patch("builtins.input", side_effect=["invalid_input", "add"])
    def test_handle_manage_selection_invalid_input(self,mock_input, mock_add, mock_print):
        self.casino.handle_manage_selection()
        mock_print.assert_called_once_with(
            self.casino.console.print_colored("Invalid input. Please try again", ANSI_COLORS.RED))
        mock_add.assert_called_once()

    @patch("builtins.input", return_value="login")
    @patch("Application.Casino.Casino.Casino.handle_login",
           return_value=UserAccount("test_username", "test_password", 50))
    def test_handle_initial_action_login(self, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account)

    @patch("builtins.input", return_value="signup")
    @patch("Application.Casino.Casino.Casino.handle_signup",
           return_value=UserAccount("test_username", "test_password", 50))
    def test_handle_initial_action_signup(self, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account, "test_username", "test_password")

    @patch("builtins.input", side_effect=["invalid_input", "signup"])
    @patch("Application.Casino.Casino.Casino.handle_signup",
           return_value=UserAccount("test_username", "test_password", 50))
    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    def test_handle_initial_action_invalid_then_signup(self, mock_print, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account, "test_username", "test_password")

    @patch("builtins.input", side_effect=["invalid_input", "login"])
    @patch("Application.Casino.Casino.Casino.handle_login",
           return_value=UserAccount("test_username", "test_password", 50))
    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    def test_handle_initial_action_login(self, mock_print, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account)



    def assert_prompt_manage_or_select(self, mock_input, mock_manage_selection):
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])
        mock_manage_selection.assert_called_once()

    def assert_account_info(self, account, expected_username="test_username", expected_password="test_password"):
        expected_username = expected_username
        expected_password = expected_password
        expected_balance = 50.0
        actual_username = account.username
        actual_password = account.password
        actual_balance = account.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)