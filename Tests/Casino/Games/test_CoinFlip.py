from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip
from Tests.BaseTest import BaseTest


class TestCoinFlip(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = self.manager.create_account("test_username", "test_password", 50.0)
        game: CoinFlip = CoinFlip(self.account, self.manager)