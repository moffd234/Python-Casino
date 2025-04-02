import unittest

from Application.Casino.AccountManager import AccountManager
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame


class test_TriviaGame(unittest.TestCase):

    def setUp(self):
        self.manager = AccountManager()
        self.game = TriviaGame(self.manager.get_account("Username", "Password"))
