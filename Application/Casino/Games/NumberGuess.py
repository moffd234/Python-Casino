import random

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Tests.Casino.Games.Game import Game


class NumberGuess(Game):
    def __init__(self, player: CasinoAccount):
        super().__init__(player)
        self.console.color = ANSI_COLORS.CYAN.value

    def print_welcome_message(self) -> str:
        return self.console.print_colored(r"""
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88b 88 88   88 8b    d8      dP""b8 88   88 888888 .dP"Y8 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88Yb88 88   88 88b  d88     dP   `" 88   88 88__   `Ybo." `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88 Y88 Y8   8P 88YbdP88     Yb  "88 Y8   8P 88""   o.`Y8b o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Y8 `YbodP' 88 YY 88      YboodP `YbodP' 888888 8bodP' 8bodP' 

        """)

    def run(self):
        num: int = random.randint(1, 10) # From 1 to 10 [inclusive]


    def get_guess(self) -> int:
        guess: int = self.console.get_integer_input("Enter your guess from 1 - 10 (inclusive)")

        while guess < 1 or guess > 10:
            print(self.console.print_colored("Number should be from 1 - 10 (inclusive)", ANSI_COLORS.RED))
            guess = self.console.get_integer_input("Enter your guess from 1 - 10")
        return guess
