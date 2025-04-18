from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess
from Tests.BaseTest import BaseTest


class TestNumberGuess(BaseTest):

    def setUp(self):
        super().setUp()
        self.player: UserAccount = UserAccount("test_username", "test_password", 50)
        self.game: NumberGuess = NumberGuess(self.player, self.manager)