from Application.Casino.AccountManager import AccountManager
from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole

class Casino:
    def __init__(self):
        self.console = IOConsole(ANSI_COLORS.BLUE)
        self.manager = AccountManager()

    def run(self) -> None:
        self.print_welcome()

        account: CasinoAccount | None = self.handle_initial_action()
        while not account:
            account = self.handle_initial_action()

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

    def handle_login(self) -> CasinoAccount | None:
        for i in range(0, 5):

            username: str = self.console.get_string_input("Enter your username", return_in_lower=False)
            password: str = self.console.get_string_input("Enter your password", return_in_lower=False)

            account: CasinoAccount | None = self.manager.get_account(username=username, password=password)

            if account:
                return account
            else:
                print("Invalid login info")
        print("Too many login attempts - returning to main screen\n\n\n")
        return None

    def handle_signup(self) -> CasinoAccount:

        while True:
            username: str = self.console.get_string_input("Create your username", return_in_lower=False)
            password: str = self.console.get_string_input("Create your password", return_in_lower=False)
            account: CasinoAccount = self.manager.create_account(username=username, password=password)
            if account:
                self.manager.register_account(account)
                return account

            else:
                print("Account with that username already exists")

    def handle_initial_action(self) -> CasinoAccount:
        answer: str = self.console.get_string_input("Welcome to the Arcade Dashboard!" +
                "\nFrom here, you can select any of the following options:" +
                "\n\t[ signup ], [ login ]")

        while True:

            if answer == "login":
                account: CasinoAccount | None = self.handle_login()
                return account

            elif answer == "signup":
                account: CasinoAccount = self.handle_signup()
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
                pass

    def prompt_game(self) -> None:
        while True:
            answer = self.console.get_string_input("Welcome to the Game Selection Dashboard!" +
                "\nFrom here, you can select any of the following options:" +
                "\n\t[ SLOTS ], [ NUMBERGUESS ], [ TRIVIA ], [ TIC-TAC-TOE ]")

            # The following are placeholders until the games are made
            if answer == "slots":
                pass

            elif answer == "numberguess":
                pass

            elif answer == "trivia":
                pass

            elif answer == "tic-tac-toe" or answer == "tictactoe":
                pass