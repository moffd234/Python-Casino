from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Slots.Slots import Slots
from Tests.BaseTest import BaseTest


class TestSlots(BaseTest):

    def setUp(self):
        super().setUp()
        self.player: UserAccount = UserAccount("test_username", "test_password", 50)
        self.game = Slots(self.player, self.manager)

    def test_print_welcome_message(self):
        expected: str = r"""        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      .dP"Y8 88      dP"Yb  888888 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     `Ybo." 88     dP   Yb   88   `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     o.`Y8b 88  .o Yb   dP   88   o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      8bodP' 88ood8  YbodP    88   8bodP' 
           
           Rules:
                - 1. Enter a wager amount.
                - 2. Match three symbols on the pay line to win
                - 3. Payouts vary based on the symbols matched:
                     - Three 7s: Jackpot(10x)
                     - Three Bells: Big Win(5x)
                     - Three Bars: Medium Win (2x)
                     - Three Cherries: Small Win (1.5x)
                     - Any other combination: No Win (You lose your wager)
        """

        actual: str = self.game.print_welcome_message()

        self.assertEqual(expected, actual)