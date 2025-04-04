import unittest

from Application.Casino.AccountManager import AccountManager
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        manager = AccountManager()
        self.game = TicTacToe(manager.get_account("Username", "Password"))

    def test_check_for_winner_horizontal(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_middle(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             [" ", " ", " "]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_last(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             ["x", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_first(self):
        self.game.game_board = \
            [["o", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_second(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_last(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "o", "x"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)