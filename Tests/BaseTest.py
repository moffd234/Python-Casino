import os.path
import unittest

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.db import init_db

IOCONSOLE_PATH: str = "Application.Utils.IOConsole.IOConsole"
GAMES_PATH: str = "Application.Casino.Games"
TRIVIA_GAME_FILE_PATH: str = f"{GAMES_PATH}.TriviaGame.TriviaGame"
TRIVIA_GAME_CLASS_PATH: str = f"{TRIVIA_GAME_FILE_PATH}.TriviaGame"
TICTACTOE_CLASS_PATH: str = f"{GAMES_PATH}.TicTacToe.TicTacToe.TicTacToe"
RPS_FILE_PATH: str = f"{GAMES_PATH}.RockPaperScissors.RPS"
SLOTS_FILE_PATH: str = f"{GAMES_PATH}.Slots.Slots"
COINFLIP_FILE_PATH: str = f"{GAMES_PATH}.CoinFlip.CoinFlip"
COINFLIP_CLASS_PATH: str = f"{COINFLIP_FILE_PATH}.CoinFlip"
NUMBERGUESS_FILE_PATH: str = f"{GAMES_PATH}.NumberGuess.NumberGuess"
NUMBERGUESS_CLASS_PATH: str = f"{NUMBERGUESS_FILE_PATH}.NumberGuess"
CASINO_CLASS_PATH: str = "Application.Casino.Casino.Casino"
ACCOUNT_MANAGER_CLASS_PATH: str = "Application.Casino.Accounts.AccountManager.AccountManager"

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.session = init_db(in_memory=True)
        self.manager = AccountManager(session=self.session)


    def tearDown(self):
        if hasattr(self.manager, 'session'):
            self.manager.session.close()

        if os.path.exists("casino.db"):
            os.remove("casino.db")

        if os.path.exists("category_cache.txt"):
            os.remove("category_cache.txt")