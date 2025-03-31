from Application.Casino.AccountManager import AccountManager
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame

if __name__ == '__main__':
    # casino = Casino()
    # casino.run()
    manager = AccountManager()
    game = TriviaGame(manager.get_account("Username", "Password"))
    game.get_difficulty()