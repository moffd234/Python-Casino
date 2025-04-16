from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.RockPaperScissors.RPS import RPS, handle_winner
from Tests.BaseTest import BaseTest


class TestRPS(BaseTest):

    def setup(self):
        super().setUp()
        account: UserAccount = self.manager.create_account("username", "password")
        self.game = RPS(account, self.manager)

    def test_handle_winner_cpu_paper(self):
        expected = "You lost! Rock loses to paper!"
        actual = handle_winner("paper", "rock")

        self.assertEqual(expected, actual)

    def test_handle_winner_cpu_scissors(self):
        expected = "You lost! Paper loses to scissors!"
        actual = handle_winner("scissors", "paper")

        self.assertEqual(expected, actual)

    def test_handle_winner_cpu_rock(self):
        expected = "You lost! Scissors loses to rock!"
        actual = handle_winner("rock", "scissors")

        self.assertEqual(expected, actual)

    def test_handle_winner_user_scissors(self):
        expected = "You won! Scissors beats paper!"
        actual = handle_winner("paper", "scissors")

        self.assertEqual(expected, actual)

    def test_handle_winner_user_paper(self):
        expected = "You won! Paper beats rock!"
        actual = handle_winner("rock", "paper")

        self.assertEqual(expected, actual)

    def test_handle_winner_user_rock(self):
        expected = "You won! Rock beats scissors!"
        actual = handle_winner("scissors", "rock")

        self.assertEqual(expected, actual)

    def test_handle_winner_draw_rock(self):
        expected = "Draw! Rock ties rock!"
        actual = handle_winner("rock", "rock")

        self.assertEqual(expected, actual)

    def test_handle_winner_draw_paper(self):
        expected = "Draw! Paper ties paper!"
        actual = handle_winner("paper", "paper")

        self.assertEqual(expected, actual)

    def test_handle_winner_draw_scissors(self):
        expected = "Draw! Scissors ties scissors!"
        actual = handle_winner("scissors", "scissors")

        self.assertEqual(expected, actual)