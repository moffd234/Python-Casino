from Application.Casino.AccountManager import AccountManager
from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole

IOConsole = IOConsole()
manager = AccountManager()

def print_welcome():
    return IOConsole.print_colored(r"""
        888       888          888                                         888 888 
        888   o   888          888                                         888 888 
        888  d8b  888          888                                         888 888 
        888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
        888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
        88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
        8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
        888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
        """, ANSI_COLORS.BLUE)

def handle_login() -> CasinoAccount:
    username: str = IOConsole.get_string_input("Enter your username\n")
    password: str = IOConsole.get_string_input("Enter your password\n")

    account: CasinoAccount | None = manager.get_account(username=username, password=password)
    while True:
        if account:
            return account
        else:
            print("Invalid login info")

