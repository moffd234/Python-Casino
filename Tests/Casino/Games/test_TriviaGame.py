import unittest

from Application.Casino.AccountManager import AccountManager
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame


class test_TriviaGame(unittest.TestCase):

    def setUp(self):
        self.manager = AccountManager()
        self.game = TriviaGame(self.manager.get_account("Username", "Password"))

    def test_get_winnings_total_hard_multiple(self):
        self.game.q_type = "multiple"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 93.75
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_hard_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 75
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_multiple(self):

        self.game.q_type = "multiple"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 78.12  # Should be rounded down from 78.125
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_tf(self):

        self.game.q_type = "boolean"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 62.5
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_multiple(self):

        self.game.q_type = "multiple"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 62.5
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 50.0
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)
