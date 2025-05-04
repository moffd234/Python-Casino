from unittest.mock import patch

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.RockPaperScissors.RPS import RPS, get_comp_turn
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, RPS_FILE_PATH


class TestRPS(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = self.manager.create_account("username", "password")
        self.game = RPS(self.account, self.manager)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_welcome(self, mock_print):
        expected: str = r"""
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88""Yb 88""Yb .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88__dP 88__dP `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88"Yb  88""''   `Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Yb 88     8bodP'
           
           Rules:
                - Normal Rock Paper Scissors rules (rock beats scissors, scissors beats paper, paper beats rock)
                - Payout is 1.25x the wager amount
        """

        self.game.print_welcome_message()

        mock_print.assert_called_with(expected)

    @patch(f"{RPS_FILE_PATH}.randint", return_value=0)
    def test_get_comp_turn_paper(self, mock_random):
        expected: str = "paper"
        actual: str = get_comp_turn()

        mock_random.assert_called_once()

        self.assertEqual(expected, actual)

    @patch(f"{RPS_FILE_PATH}.randint", return_value=1)
    def test_get_comp_turn_scissors(self, mock_random):
        expected: str = "scissors"
        actual: str = get_comp_turn()

        mock_random.assert_called_once()

        self.assertEqual(expected, actual)

    @patch(f"{RPS_FILE_PATH}.randint", return_value=2)
    def test_get_comp_turn_rock(self, mock_random):
        expected: str = "rock"
        actual: str = get_comp_turn()

        mock_random.assert_called_once()

        self.assertEqual(expected, actual)

    def test_handle_winner_cpu_paper(self):
        expected_output = "You lost! Rock loses to paper!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("paper", "rock", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_cpu_scissors(self):
        expected_output = "You lost! Paper loses to scissors!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("scissors", "paper", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_cpu_rock(self):
        expected_output = "You lost! Scissors loses to rock!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("rock", "scissors", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_user_scissors(self):
        expected_output = "You won! Scissors beats paper!"
        expected_balance = round(self.account.balance + (10 * 1.25), 2)

        actual_output = self.game.handle_winner("paper", "scissors", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_user_paper(self):
        expected_output = "You won! Paper beats rock!"
        expected_balance = round(self.account.balance + (10 * 1.25), 2)

        actual_output = self.game.handle_winner("rock", "paper", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_user_rock(self):
        expected_output = "You won! Rock beats scissors!"
        expected_balance = round(self.account.balance + (10 * 1.25), 2)

        actual_output = self.game.handle_winner("scissors", "rock", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_draw_rock(self):
        expected_output = "Draw! Rock ties rock!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("rock", "rock", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_draw_paper(self):
        expected_output = "Draw! Paper ties paper!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("paper", "paper", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_winner_draw_scissors(self):
        expected_output = "Draw! Scissors ties scissors!"
        expected_balance = self.account.balance

        actual_output = self.game.handle_winner("scissors", "scissors", 10)
        actual_balance = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    @patch("builtins.input", return_value="rock")
    def test_get_user_turn_rock(self, mocked_input):
        expected: str = "rock"
        actual: str = self.game.get_user_turn()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="ROCK")
    def test_get_user_turn_rock_capitalized(self, mocked_input):
        expected: str = "rock"
        actual: str = self.game.get_user_turn()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="paper")
    def test_get_user_turn_paper(self, mocked_input):
        expected: str = "paper"
        actual: str = self.game.get_user_turn()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="scissors")
    def test_get_user_turn_scissors(self, mocked_input):
        expected: str = "scissors"
        actual: str = self.game.get_user_turn()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["ss", "scissors"])
    def test_get_user_turn_incorrect_value(self, mock_input):
        expected: str = "scissors"
        actual: str = self.game.get_user_turn()
        expected_call_count: int = 2
        actual_call_count: int = mock_input.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)