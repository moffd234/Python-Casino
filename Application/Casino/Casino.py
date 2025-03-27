from Application.Casino.AccountManager import AccountManager
from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole

class Casino:
    def __init__(self):
        self.console = IOConsole()
        self.manager = AccountManager()

    def print_welcome(self):
        return self.console.print_colored(r"""
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            """, ANSI_COLORS.BLUE)

    def handle_login(self) -> CasinoAccount | None:
        username: str = self.console.get_string_input("Enter your username\n")
        password: str = self.console.get_string_input("Enter your password\n")

        account: CasinoAccount | None = self.manager.get_account(username=username, password=password)
        for i in range(0, 5):
            if account:
                return account
            else:
                print("Invalid login info")
        print("Too many login attempts - returning to main screen")
        return None
