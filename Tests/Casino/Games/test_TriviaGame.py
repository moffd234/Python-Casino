import unittest

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame


class test_TriviaGame(unittest.TestCase):

    def setUp(self):
        self.manager = AccountManager()
        self.game = TriviaGame(self.manager.get_account("Username", "Password"), self.manager)
        self.test_question_tf = Question("is this how to spell true 'true'?", "true", ["false"])
        self.test_question_mc = Question("What is the first letter of the alphabet'?",
                                         "a", ["b", "c", "d"])

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

    def test_check_answer_tf_true(self):
        self.game.score = 0
        self.game.check_answer("true", self.test_question_tf, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_right(self):
        self.game.score = 0
        self.game.check_answer("a", self.test_question_mc, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_wrong(self):
        self.game.score = 0
        self.game.check_answer("c", self.test_question_mc, 1)

        expected: int = 0
        actual = self.game.score

        self.assertEqual(expected, actual)
