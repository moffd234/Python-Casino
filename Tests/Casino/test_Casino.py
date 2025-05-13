from unittest.mock import patch, call

from Application.Casino.Casino import *
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, COINFLIP_FILE_PATH, GAMES_PATH, SLOTS_FILE_PATH, CASINO_CLASS_PATH, \
    ACCOUNT_MANAGER_CLASS_PATH, TEST_QUESTIONS
from Tests.Casino.Games.test_RPS import RPS_FILE_PATH
from Tests.Casino.Games.test_TicTacToe import TICTACTOE_CLASS_PATH
from Tests.Casino.Games.test_TriviaGame import TRIVIA_GAME_CLASS_PATH


class TestCasino(BaseTest):

    def setUp(self):
        super().setUp()
        self.casino = Casino()
        self.casino.account = self.account

    def assert_prompt_game(self, mock_input, mock_run):
        self.casino.prompt_game()
        mock_input.assert_has_calls([call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")])
        mock_run.assert_called_once()

    def assert_prompt_manage_or_select(self, mock_input, mock_selection):
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])
        mock_selection.assert_called_once()

    def assert_account_info(self, account, expected_username="test_username", expected_password="ValidPassword123!"):
        expected_username = expected_username
        expected_password = expected_password
        expected_balance = 50.0
        actual_username = account.username
        actual_password = account.password
        actual_balance = account.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)

    @patch("builtins.print")
    def test_print_welcome(self, mock_print):
        expected: str = r"""[34m
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            
            Notes:
                - At anypoint you can exit the application by typing "exit"
                - Funds can be added and you can reset you password from the manage account screen after logging in
            """
        self.casino.print_welcome()
        mock_print.assert_called_with(expected)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account",
           return_value=UserAccount("test_username", "ValidPassword123!", 50.0,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["test_username", "ValidPassword123!"])
    def test_handle_login(self, mock_inputs, mock_get_account):
        account: UserAccount = self.casino.handle_login()

        self.assert_account_info(account)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account", return_value=None)
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["wrong_user", "wrong_pass"] * 5)
    def test_handle_login_fail(self, mock_get_string_input, mock_get_account):
        account = self.casino.handle_login()
        self.assertIsNone(account)

    @patch(f"Application.Casino.Casino.is_password_valid")
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.create_account",
           return_value=UserAccount("test_username", "ValidPassword123!", 50.0,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["test_username", "ValidPassword123!"])
    def test_handle_signup(self, mock_inputs, mock_get_account, mock_is_password_valid):
        account: UserAccount = self.casino.handle_signup()

        mock_is_password_valid.assert_called_once_with("ValidPassword123!")
        self.assert_account_info(account)

    @patch(f"Application.Casino.Casino.is_password_valid", side_effect=[True, True])
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.create_account",
           side_effect=[None, UserAccount("test_username", "ValidPassword123!", 50.0,
                                          "test@email.com", TEST_QUESTIONS)])
    @patch(f"{IOCONSOLE_PATH}.get_string_input",
           side_effect=["test_username", "ValidPassword123!", "test_username", "ValidPassword1234!"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_signup_account_exist(self, mock_print, mock_inputs, mock_create_account, mock_is_password_valid):
        account: UserAccount = self.casino.handle_signup()

        mock_print.assert_called_once_with("Account with that username already exists")
        mock_is_password_valid.assert_has_calls([call("ValidPassword123!"), call("ValidPassword1234!")])
        self.assertEqual(mock_is_password_valid.call_count, 2)

        self.assert_account_info(account)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="back")
    def test_handle_signup_username_back(self, mock_input):
        actual: None = self.casino.handle_signup()

        mock_input.assert_called_once_with("Create your username or type back", return_in_lower=False)

        self.assertIsNone(actual)

    @patch("builtins.print")
    @patch("builtins.input", return_value="50")
    def test_handle_add_funds(self, mock_input, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()

        actual_balance: float = self.casino.account.balance

        mock_print.assert_called_once_with(f"{ANSI_COLORS.GREEN.value}You have added $50.0 to your funds!"
                                           f" New Balance is {self.casino.account.balance}")
        self.assertEqual(expected_balance, actual_balance)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=["-1", "50"])
    def test_handle_add_funds_negative(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=[".99", "50"])
    def test_handle_add_funds_low_decimal(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    def add_funds_and_assert(self, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()
        actual_balance: float = self.casino.account.balance
        mock_print.assert_has_calls([
            call("Please enter a valid amount "
                 "(A positive number >= 1.00 with no more than 2 decimal places).",
                 ANSI_COLORS.RED),
            call(
                f"You have added $50.0 to your funds! New Balance is {self.casino.account.balance}", ANSI_COLORS.GREEN)
        ])
        self.assertEqual(expected_balance, actual_balance)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=["password", "ValidPassword123!"])
    def test_reset_password(self, mock_input, mock_print):
        self.casino.reset_password()

        expected_password = "ValidPassword123!"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        self.assertEqual(expected_password, actual_password)

    @patch(f"{CASINO_CLASS_PATH}.update_password")
    @patch("builtins.input", side_effect=["password", "ValidPassword123!"])
    def test_reset_password_assert_update_called(self, mock_input, mock_update_password):
        self.casino.reset_password()

        expected_password = "ValidPassword123!"

        mock_update_password.assert_called_once_with(expected_password)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=["test_pAsSwOrD123!", "ValidPassword123!"])
    def test_reset_password_case_sensitive(self, mock_input, mock_print):
        account: UserAccount = self.casino.manager.create_account("test_username", "test_pAsSwOrD123!")
        self.casino.account = account
        self.casino.reset_password()

        expected_password = "ValidPassword123!"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with(f"Your password has been updated!", ANSI_COLORS.GREEN)
        self.assertEqual(expected_password, actual_password)

    @patch(f"{IOCONSOLE_PATH}.print_error")
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

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch("builtins.input", side_effect=["wrong_password", "wrong_password", "password", "ValidPassword123!"])
    def test_reset_password_failed_then_works(self, mock_input, mock_print_error, mock_print):
        self.casino.reset_password()

        expected_password: str = "ValidPassword123!"
        actual_password = self.casino.account.password

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_print_error.assert_has_calls([
            call("Passwords do not match"),
            call("Passwords do not match")
        ])
        self.assertEqual(expected_password, actual_password)

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add")
    def test_handle_manage_selection_add(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add-funds")
    def test_handle_manage_selection_add_dash_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add funds")
    def test_handle_manage_selection_add_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
    @patch("builtins.input", return_value="reset")
    def test_handle_manage_selection_reset(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
    @patch("builtins.input", return_value="reset password")
    def test_handle_manage_selection_reset_password(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
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

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", side_effect=["invalid_input", "add"])
    def test_handle_manage_selection_invalid_input(self, mock_input, mock_add, mock_print):
        self.casino.handle_manage_selection()
        mock_print.assert_called_once_with("Invalid input. Please try again")
        mock_add.assert_called_once()

    @patch("builtins.input", return_value="login")
    @patch(f"{CASINO_CLASS_PATH}.handle_login",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_login(self, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account)

    @patch("builtins.input", return_value="signup")
    @patch(f"{CASINO_CLASS_PATH}.handle_signup",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_signup(self, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account, "test_username", "ValidPassword123!")

    @patch("builtins.input", side_effect=["invalid_input", "signup"])
    @patch(f"{CASINO_CLASS_PATH}.handle_signup",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_initial_action_invalid_then_signup(self, mock_print, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account, "test_username", "ValidPassword123!")

    @patch("builtins.input", side_effect=["invalid_input", "login"])
    @patch(f"{CASINO_CLASS_PATH}.handle_login",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_initial_action_login_with_invalid(self, mock_print, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage account", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage_account(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage-account", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage_dash_account(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select game", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_game(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select game", "logout"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_game_invalid_funds(self, mock_selection, mock_print, mock_input):
        self.casino.account.balance = 0.00
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select-game", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_dash_game(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["logout"])
    def test_prompt_manage_or_select_logout(self, mock_input):
        self.assertIsNone(self.casino.prompt_manage_or_select())
        mock_input.assert_called_once_with('You are logged in!\nFrom here, you can select any of the following options:'
                                           '\n\t[ manage-account ], [ select-game ], [ logout ]')

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input", "logout"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_manage_or_select_invalid_input(self, mock_print, mock_input):
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["rps", "back"])
    @patch(f"{RPS_FILE_PATH}.RPS.run", return_value=None)
    def test_prompt_game_rps(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["rock paper scissors", "back"])
    @patch(f"{RPS_FILE_PATH}.RPS.run", return_value=None)
    def test_prompt_game_rock_paper_scissors(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["numberguess", "back"])
    @patch(f"{GAMES_PATH}.NumberGuess.NumberGuess.NumberGuess.run", return_value=None)
    def test_prompt_game_numberguess(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["number guess", "back"])
    @patch(f"{GAMES_PATH}.NumberGuess.NumberGuess.NumberGuess.run", return_value=None)
    def test_prompt_game_number_guess(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["trivia", "back"])
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_trivia(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["tic-tac-toe", "back"])
    @patch(f"{TICTACTOE_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_tic_tac_toe_dashes(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["tictactoe", "back"])
    @patch(f"{TICTACTOE_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_tictactoe(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["coinflip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    def test_prompt_game_coinflip(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["coin flip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    def test_prompt_game_coin_flip(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["slots", "back"])
    @patch(f"{SLOTS_FILE_PATH}.Slots.run", return_value=None)
    def test_prompt_game_slots(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="back")
    def test_prompt_game_back(self, mock_input):
        self.casino.prompt_game()
        mock_input.assert_called_once_with("Welcome to the Game Selection Dashboard!" +
                                           "\nFrom here, you can select any of the following options:" +
                                           "\n\t[ RPS ], [ NUMBERGUESS ],"
                                           " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input",
                                                              "coin flip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_game_invalid_input(self, mock_print, mock_run, mock_input):
        self.casino.prompt_game()
        mock_input.assert_has_calls([call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")
                                     ])
        mock_run.assert_called_once()
        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")

    def test_is_password_valid_true(self):
        test_password: str = "validPassword123!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_exactly_8_chars(self):
        test_password: str = "validP1!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_too_short(self):
        test_password: str = "validPa"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_uppercase(self):
        test_password: str = "valid_password123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_lowercase(self):
        test_password: str = "VALID_PASSWORD123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_only_letters(self):
        test_password: str = "vAlIdPaSsWoRd"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_number(self):
        test_password: str = "validPassword!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_number(self):
        test_password: str = "12345678"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_special(self):
        test_password: str = "validPassword123"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_special(self):
        test_password: str = "!@#$%^&*("

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_space_char(self):
        test_password: str = "ValidPassword  123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_tab_char(self):
        test_password: str = "ValidPassword\t123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_empty_string(self):
        test_password: str = ""

        self.assertFalse(is_password_valid(test_password))

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_update_password_valid(self, mock_print, mock_update):
        self.casino.update_password("ValidPassword123!")

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_update.assert_called_once()

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="ValidPassword123!")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_update_password_fail_then_valid(self, mock_print, mock_print_error, mock_input, mock_update):
        self.casino.update_password("invalid_password")

        mock_print_error.assert_called_once_with("Invalid password. Password must follow the following:\n"
                                                 "- At least 8 characters long\n"
                                                 "- At least one uppercase letter\n"
                                                 "- At least one lowercase letter\n"
                                                 "- At least one number\n"
                                                 "- At least one special character")
        mock_input.assert_called_once_with("Enter new password: ", return_in_lower=False)
        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_update.assert_called_once()

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["none", "none", "none", "none", "none"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_update_password_max_fail(self, mock_print_error, mock_input, mock_update):
        self.casino.update_password("invalid_password")

        expected_error: str = "Invalid password. Password must follow the following:\n" \
                              "- At least 8 characters long\n" \
                              "- At least one uppercase letter\n" \
                              "- At least one lowercase letter\n" \
                              "- At least one number\n" \
                              "- At least one special character"

        mock_print_error.assert_has_calls([
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call("Too many invalid attempts. Password was not updated.")])

        mock_input.assert_has_calls([
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False)])

        mock_update.assert_not_called()

    @patch(f"{CASINO_CLASS_PATH}.print_welcome")
    @patch(f"{CASINO_CLASS_PATH}.prompt_manage_or_select")
    @patch(f"{CASINO_CLASS_PATH}.handle_initial_action", return_value=UserAccount("test_usr",
                                                                                  "ValidPass123!",
                                                                                  50.0,
                                                                                  "test@email.com", TEST_QUESTIONS))
    def test_run_valid_account(self, mock_action, mock_prompt, mock_print):
        self.casino.run()

        mock_action.assert_called_once()
        mock_prompt.assert_called_once()
        mock_print.assert_called_once()

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=1)
    def test_get_security_question(self, mock_input, mock_print):
        possible_questions: list[str] = ["question zero", "question one", "question two", "question three"]

        expected: str = "question one"
        actual: str = self.casino.get_security_question(possible_questions)
        expected_print_count: int = len(possible_questions) + 1
        print_count: int = mock_print.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_print_count, print_count)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch("builtins.input", side_effect=['-1', "1"])
    def test_get_security_question_invalid(self, mock_input, mock_print_error, mock_print):
        possible_questions: list[str] = ["question zero", "question one", "question two", "question three"]

        expected: str = "question one"
        actual: str = self.casino.get_security_question(possible_questions)
        expected_print_count: int = len(possible_questions) + 1
        print_count: int = mock_print.call_count

        mock_print_error.assert_called_once_with("Invalid input. Please enter a number from the list.")
        self.assertEqual(expected, actual)
        self.assertEqual(expected_print_count, print_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=['test_answer', "test_answer"])
    @patch(f"{CASINO_CLASS_PATH}.get_security_question",
           side_effect=["What street did you grow up on?", "What was the name of your first pet?"])
    def test_get_security_questions_and_answers(self, mock_get_questions, mock_input):
        expected: list[str] = ["What street did you grow up on?", "test_answer",
                               "What was the name of your first pet?", "test_answer"]
        actual: list[str] = self.casino.get_security_questions_and_answers()
        expected_mock_get_questions_call_count: int = 2
        actual_mock_get_questions_call_count: int = mock_get_questions.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_mock_get_questions_call_count, actual_mock_get_questions_call_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="test_username")
    def test_prompt_username(self, mock_input):
        expected: str = "test_username"
        actual: str = self.casino.prompt_username()

        mock_input.assert_called_once_with("Create your username or type back", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="back")
    def test_prompt_username_back(self, mock_input):
        actual: None = self.casino.prompt_username()

        mock_input.assert_called_once_with("Create your username or type back", return_in_lower=False)
        self.assertIsNone(actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="ValidPass123!")
    def test_prompt_password(self, mock_input):
        expected: str = "ValidPass123!"
        actual: str = self.casino.prompt_password()

        mock_input.assert_called_once_with("Create your password: ", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input",
           side_effect=["invalid_password", "ValidPassword123!"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_password_invalid(self, mock_print, mock_inputs):
        expected: str = "ValidPassword123!"
        actual: str = self.casino.prompt_password()

        mock_print.assert_called_once_with("Invalid password. Password must follow the following:\n"
                                           "- At least 8 characters long\n"
                                           "- At least one uppercase letter\n"
                                           "- At least one lowercase letter\n"
                                           "- At least one number\n"
                                           "- At least one special character")

        expected_call_count: int = 2
        actual_call_count: int = mock_inputs.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="email@testdomain.com")
    def test_prompt_email_valid(self, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_input.assert_called_once_with("Enter your email: ", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["@testdomain.com", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_char_before_at(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["emailtestdomain.com", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_at(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomaincom", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_char_after_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.c", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_one_char_after_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.c",
                                                              "emailtestdomain.com",
                                                              "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_multiple_invalid(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_has_calls([call("Invalid email."), call("Invalid email.")])
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)
