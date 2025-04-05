from abc import ABC, abstractmethod

from Application.Casino.AccountManager import AccountManager
from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole


class Game(ABC):
    def __init__(self, player: CasinoAccount, manager: AccountManager):
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
            print(self.console.print_colored(f"Wager amount must be between $1.00 - ${self.player.balance}",
                                             ANSI_COLORS.RED))
            amount = self.console.get_float_input("Enter a wager amount")

        return amount

    def get_continue_input(self) -> bool:
        return self.console.get_boolean_input("Would you like to keep playing?")