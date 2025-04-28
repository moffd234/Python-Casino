from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game


class Slots(Game):

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)

    def print_welcome_message(self) -> str:
        pass

    def run(self):
        pass