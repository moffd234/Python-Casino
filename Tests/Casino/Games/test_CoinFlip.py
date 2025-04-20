from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip
from Tests.BaseTest import BaseTest


class TestCoinFlip(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = self.manager.create_account("test_username", "test_password")
        self.game: CoinFlip = CoinFlip(self.account, self.manager)

    def test_print_welcome(self):
        expected: str = r"""[34m
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb       dP""b8  dP"Yb  88 88b 88     888888 88     88 88""Yb 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     dP   `" dP   Yb 88 88Yb88     88__   88     88 88__dP 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     Yb      Yb   dP 88 88 Y88     88""   88  .o 88 88
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP       YboodP  YbodP  88 88  Y8     88     88ood8 88 88     
        
        rules:
             1. Enter a guess of either heads or tails
             2. A coin will be flipped
             3. If you guess correctly you will win 1.25x your wager
        """

        actual: str = self.game.print_welcome_message()

        self.assertEqual(expected, actual)