from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess
from Tests.BaseTest import BaseTest


class TestNumberGuess(BaseTest):

    def setUp(self):
        super().setUp()
        self.player: UserAccount = UserAccount("test_username", "test_password", 50)
        self.game: NumberGuess = NumberGuess(self.player, self.manager)

    def test_print_welcome_message(self):
        expected: str = r"""[36m
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88b 88 88   88 8b    d8      dP""b8 88   88 888888 .dP"Y8 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88Yb88 88   88 88b  d88     dP   `" 88   88 88__   `Ybo." `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88 Y88 Y8   8P 88YbdP88     Yb  "88 Y8   8P 88""   o.`Y8b o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Y8 `YbodP' 88 YY 88      YboodP `YbodP' 888888 8bodP' 8bodP' 
           
           Rules:
                1. A random integer will be generated from 1 to 10 (including 1 and 10)
                2. You will get one chance to input a guess
                3. If you are right you will win 2x your wager
        """
        actual: str = self.game.print_welcome_message()
        self.assertEqual(expected, actual)

    def test_handle_guess_right(self):
        expected_output: str = "You Won! The answer was 5"
        expected_balance: float = self.player.balance + 20

        actual_output: str = self.game.handle_guess(5, 5, 10)
        actual_balance: float = self.player.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_guess_wrong(self):
        expected_output: str = "You lost. The answer was 5"
        expected_balance: float = self.player.balance

        actual_output: str = self.game.handle_guess(6, 5, 10)
        actual_balance: float = self.player.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)