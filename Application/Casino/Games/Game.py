from abc import ABC, abstractmethod

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Utils.IOConsole import IOConsole


class Game(ABC):
    def __init__(self, player: UserAccount, manager: AccountManager):
        self.player = player
        self.console = IOConsole()
        self.manager = manager

    @abstractmethod
    def print_welcome_message(self) -> str:
        pass

    @abstractmethod
    def run(self):
        pass

    def get_wager_amount(self) -> float:
        amount: float = self.console.get_float_input("Enter a wager amount")

        while amount > self.player.balance or amount < 1.00:
            self.console.print_error(f"Wager amount must be between $1.00 - ${self.player.balance}")
            amount = self.console.get_float_input("Enter a wager amount")

        return amount

    def get_continue_input(self) -> bool:
        return self.console.get_boolean_input("Would you like to keep playing?")