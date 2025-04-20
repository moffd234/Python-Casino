from unittest.mock import patch

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip, handle_heads_tails
from Tests.BaseTest import BaseTest


class TestCoinFlip(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = self.manager.create_account("test_username", "test_password")
        self.game: CoinFlip = CoinFlip(self.account, self.manager)

    def test_print_welcome(self):
        expected: str = r"""[34m
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb       dP""b8  dP"Yb  88 88b 88     888888 88     88 88""Yb 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     dP   `" dP   Yb 88 88Yb88     88__   88     88 88__dP 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     Yb      Yb   dP 88 88 Y88     88""   88  .o 88 88
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP       YboodP  YbodP  88 88  Y8     88     88ood8 88 88     
        
        rules:
             1. Enter a guess of either heads or tails
             2. A coin will be flipped
             3. If you guess correctly you will win 1.25x your wager
        """

        actual: str = self.game.print_welcome_message()

        self.assertEqual(expected, actual)

    @patch("Application.Casino.Games.CoinFlip.CoinFlip.random.randint", return_value=0)
    def test_handle_heads_tails_zero(self, mock_randint):
        expected: str = "tails"
        actual: str = handle_heads_tails()

        self.assertEqual(expected, actual)

    @patch("Application.Casino.Games.CoinFlip.CoinFlip.random.randint", return_value=1)
    def test_handle_heads_tails_one(self, mock_randint):
        expected: str = "heads"
        actual: str = handle_heads_tails()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="tails")
    def test_get_guess_tails(self, mock_input):
        expected: str = "tails"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="heads")
    def test_get_guess_heads(self, mock_input):
        expected: str = "heads"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["invalid_input","tails"])
    def test_get_guess_invalid_tails(self, mock_input):
        expected: str = "tails"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["invalid_input", "heads"])
    def test_get_guess_invalid_heads(self, mock_input):
        expected: str = "heads"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    def test_handle_outcome_win_tails(self):
        expected_output: str = "You Won! The coin was tails"
        expected_balance: float = self.account.balance + (10 * 1.25)

        actual_output: str = self.game.handle_outcome("tails", "tails", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_outcome_win_heads(self):
        expected_output: str = "You Won! The coin was heads"
        expected_balance: float = self.account.balance + (10 * 1.25)

        actual_output: str = self.game.handle_outcome("heads", "heads", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_outcome_loss_tails_guess(self):
        expected_output: str = "You Loss! The coin was heads"
        expected_balance: float = self.account.balance

        actual_output: str = self.game.handle_outcome("tails", "heads", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_outcome_loss_heads_guess(self):
        expected_output: str = "You Loss! The coin was tails"
        expected_balance: float = self.account.balance

        actual_output: str = self.game.handle_outcome("heads", "tails", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)