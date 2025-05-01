from unittest.mock import patch, call

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Slots.Slots import Slots, get_spin, handle_spin, get_payout
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

    def test_get_spin(self):
        expected_len: int = 3
        actual_len: int = len(get_spin())

        outcomes: set[str] = set()
        possibilities: list[str] = ["7️⃣", "🔔", "⬛", "🍒"]

        for _ in range(1000):
            outcomes.add(get_spin()[0])
            outcomes.add(get_spin()[1])
            outcomes.add(get_spin()[2])

        for sym in possibilities:
            self.assertIn(sym, outcomes)

        self.assertEqual(expected_len, actual_len)

    def test_handle_spin_no_win(self):
        syms: list[str] = ["🔔", "🔔", "⬛"]

        expected: float = 0
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_7_win(self):
        syms: list[str] = ["7️⃣", "7️⃣", "7️⃣"]

        expected: float = 10
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_bell_win(self):
        syms: list[str] = ["🔔", "🔔", "🔔"]

        expected: float = 5
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_bar_win(self):
        syms: list[str] = ["⬛", "⬛", "⬛"]

        expected: float = 2
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_cherry_win(self):
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 1.5
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    @patch("Application.Casino.Games.Slots.Slots.handle_spin")
    def test_get_payout_assert_mock_called(self, mock_handle_spin):
        spin: list[str] = ["🔔", "🔔", "⬛"]
        get_payout(10, spin)

        mock_handle_spin.assert_called_once_with(spin)

    def test_get_payout_none(self):
        expected: float = 0

        spin: list[str] = ["🔔", "🔔", "⬛"]
        actual: float = get_payout(10, spin)

        self.assertEqual(expected, actual)

    def test_get_payout_7_win(self):
        syms: list[str] = ["7️⃣", "7️⃣", "7️⃣"]

        expected: float = 100.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_bell_win(self):
        syms: list[str] = ["🔔", "🔔", "🔔"]

        expected: float = 50.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_bar_win(self):
        syms: list[str] = ["⬛", "⬛", "⬛"]

        expected: float = 20.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_cherry_win(self):
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 15.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_round_up(self):
        # There is no round down test as that shouldn't be able to occur
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 15.50
        actual: float = get_payout(10.33, syms)

        self.assertEqual(expected, actual)

    @patch("Application.Utils.IOConsole.IOConsole.print_colored")
    def test_print_spin(self, mock_print):
        self.game.print_spin(["🍒", "🍒", "🍒"])

        expected_calls = [
            call("\n🎰 Spinning... 🎰\n"),
            call("┌───┬───┬───┐"),
            call("│ 🍒│ 🍒│ 🍒│"),
            call("└───┴───┴───┘\n"),
        ]

        # Only compare the arguments passed to print_colored directly
        actual_calls = mock_print.call_args_list
        self.assertEqual(actual_calls, expected_calls)
