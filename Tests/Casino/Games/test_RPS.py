from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.RockPaperScissors.RPS import RPS
from Tests.BaseTest import BaseTest


class TestRPS(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = self.manager.create_account("username", "password")
        self.game = RPS(self.account, self.manager)

    def test_print_welcome(self):
        expected: str = r"""
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88""Yb 88""Yb .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88__dP 88__dP `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88"Yb  88""''   `Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Yb 88     8bodP'
           
           Rules:
                - Normal Rock Paper Scissors rules (rock beats scissors, scissors beats paper, paper beats rock)
                - Payout is 1.25x the wager amount
        """

        actual: str = self.game.print_welcome_message()
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