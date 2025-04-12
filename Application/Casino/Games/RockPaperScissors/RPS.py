from random import randint

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game


def get_comp_turn() -> str:
    ran_num = randint(0, 2)
    if ran_num == 0:
        return "Paper"
    elif ran_num == 1:
        return "Scissors"
    else:
        return "Rock"

class RPS(Game):
    def print_welcome_message(self) -> str:
        pass

    def run(self):
        pass

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)


    def get_turn(self) -> str:
        turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        while turn != "Rock" and turn != "Paper" and turn != "Scissors":
            turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        return turn

