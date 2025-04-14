from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip
from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess
from Application.Casino.Games.RockPaperScissors.RPS import RPS
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole

class Casino:
    def __init__(self):
        self.console = IOConsole(ANSI_COLORS.BLUE)
        self.manager = AccountManager()
        self.account:  UserAccount | None = None

    def run(self) -> None:
        self.print_welcome()

        self.account = self.handle_initial_action()
        while not self.account:
            self.account = self.handle_initial_action()

        self.prompt_manage_or_select()

    def print_welcome(self) -> str:
        return self.console.print_colored(r"""
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            """)

    def handle_login(self) -> UserAccount | None:
        for i in range(0, 5):

            username: str = self.console.get_string_input("Enter your username", return_in_lower=False)
            password: str = self.console.get_string_input("Enter your password", return_in_lower=False)

            account: UserAccount | None = self.manager.get_account(username=username, password=password)

            if account:
                return account
            else:
                print(self.console.print_colored("Invalid login info", ANSI_COLORS.RED))

        print("Too many login attempts - returning to main screen\n\n\n")
        return None

    def handle_signup(self) -> UserAccount:

        while True:
            username: str = self.console.get_string_input("Create your username", return_in_lower=False)
            password: str = self.console.get_string_input("Create your password", return_in_lower=False)
            account: UserAccount = self.manager.create_account(username=username, password=password)
            if account:
                return account

            else:
                print(self.console.print_colored("Account with that username already exists"), ANSI_COLORS.RED)

    def handle_initial_action(self) -> UserAccount:
        answer: str = self.console.get_string_input("Welcome to the Arcade Dashboard!" +
                "\nFrom here, you can select any of the following options:" +
                "\n\t[ signup ], [ login ]")

        while True:

            if answer == "login":
                account: UserAccount | None = self.handle_login()
                return account

            elif answer == "signup":
                account: UserAccount = self.handle_signup()
                return account

            else:
                answer = self.console.get_string_input("Invalid input. Please try again")

    def prompt_manage_or_select(self) -> None:
        while True:
            answer = self.console.get_string_input("You are logged in!" +
                "\nFrom here, you can select any of the following options:" +
                "\n\t[ manage-account ], [ select-game ]")

            if answer == "manage-account" or answer == "manage account" or answer == "manage":
                pass

            elif answer == "select-game" or answer == "select game" or answer == "select":
                if self.account.balance < 1.00:
                    print(self.console.print_colored("You do not have enough money to play any games"), ANSI_COLORS.RED)
                else:
                    self.prompt_game()

    def prompt_game(self) -> None:
        while True:
            answer = self.console.get_string_input("Welcome to the Game Selection Dashboard!" +
                "\nFrom here, you can select any of the following options:" +
                "\n\t[ RPS ], [ NUMBERGUESS ], [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ]")

            # The following are placeholders until the games are made
            if answer == "rps":
                game = RPS(self.account, self.manager)
                game.run()

            elif answer == "numberguess":
                game = NumberGuess(self.account, self.manager)
                game.run()

            elif answer == "trivia":
                game = TriviaGame(self.account, self.manager)
                game.run()

            elif answer == "tic-tac-toe" or answer == "tictactoe":
                game = TicTacToe(self.account, self.manager)
                game.run()

            elif answer == "coinflip" or answer == "coin flip":
                game = CoinFlip(self.account, self.manager)
                game.run()

            elif answer == "back":
                return None

    def add_funds(self) -> None:
        while True:
            answer: float = self.console.get_float_input("Enter the amount of money you want to add to your funds"
                                                  " (Up to $100 but no less than $.01)")
            if 0 < answer < 100:
                self.manager.add_and_save_account(self.account, answer)
                print(self.console.print_colored(f"You have added {answer} to your funds! "
                                                 f"New Balance is {self.account.balance}", ANSI_COLORS.GREEN))
                return None

            print(self.console.print_colored("Invalid input. Please try again", ANSI_COLORS.RED))