from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Slots.Slots import Slots
from Tests.BaseTest import BaseTest


class TestSlots(BaseTest):

    def setUp(self):
        super().setUp()
        self.player: UserAccount = UserAccount("test_username", "test_password", 50)
        self.game = Slots(self.player, self.manager)
