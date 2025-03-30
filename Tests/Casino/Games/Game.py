from abc import ABC, abstractmethod

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.IOConsole import IOConsole


class Game(ABC):
    def __init__(self, player: CasinoAccount):
        self.player = player
        self.console = IOConsole()

    @abstractmethod
    def print_welcome_message(self) -> str:
        pass

    @abstractmethod
    def run(self):
        pass

    def get_wager_amount(self):
        amount: float = self.console.get_float_input("Enter a wager amount")

        while amount > self.player.balance or amount < 1.00:
            print(f"Wager amount must be between $1.00 - {self.player.balance}")
            amount = self.console.get_float_input("Enter a wager amount")

        return amount