from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.IOConsole import IOConsole

if __name__ == '__main__':
    casinoAccount = CasinoAccount("abc", "abc", 45)
    casinoAccount.add_winnings(-12)
