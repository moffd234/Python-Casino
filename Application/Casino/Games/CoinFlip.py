from Application.Casino.CasinoAccount import CasinoAccount
from Application.Casino.Games.Game import Game


class CoinFlip(Game):
    def print_welcome_message(self) -> str:
        pass

    def run(self):
        pass

    def __init__(self, player: CasinoAccount):
        super().__init__(player)