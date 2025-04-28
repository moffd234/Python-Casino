from unittest.mock import patch
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe
from Tests.BaseTest import BaseTest

class TestTicTacToe(BaseTest):

    def setUp(self):
        super().setUp()
        self.game = TicTacToe(self.manager.get_account("Username", "Password"), self.manager)

    def test_print_welcome_message(self):
        expected: str = r"""[36m
         __          __  _                            _______      _______ _          _______             _______         
         \ \        / / | |                          |__   __|    |__   __(_)        |__   __|           |__   __|        
          \ \  /\  / /__| | ___ ___  _ __ ___   ___     | | ___      | |   _  ___ ______| | __ _  ___ ______| | ___   ___ 
           \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \    | |/ _ \     | |  | |/ __|______| |/ _` |/ __|______| |/ _ \ / _ \
            \  /\  /  __/ | (_| (_) | | | | | |  __/    | | (_) |    | |  | | (__       | | (_| | (__       | | (_) |  __/
             \/  \/ \___|_|\___\___/|_| |_| |_|\___|    |_|\___/     |_|  |_|\___|      |_|\__,_|\___|      |_|\___/ \___|
                                                                                                                          
            
            Rules:
                This is a non-gambling game so you will not win or lose money.
                Two players take turns placing their symbol on the board.
                The first player to place three of their symbols in a horizontal, vertical, or diagonal row wins.                                                                                                    
        """

        actual: str = self.game.print_welcome_message()

        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_middle(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             [" ", " ", " "]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_last(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             ["x", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_first(self):
        self.game.game_board = \
            [["o", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_second(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_last(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "o", "x"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_diagonal_bottom_to_top(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["o", "x", "o"],
             ["x", "o", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_diagonal_top_to_bottom(self):
        self.game.game_board = \
            [["x", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_none(self):
        self.game.game_board = \
            [["x", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "o"]]

        expected: None = None
        actual: None = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_is_cell_empty_false(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        actual: bool = self.game.is_cell_empty(0, 0)
        self.assertFalse(actual)

    def test_is_cell_empty_true(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        actual: bool = self.game.is_cell_empty(1, 0)
        self.assertTrue(actual)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", return_value=1)
    def test_get_row_first_try(self, mock_input):
        expected: int = 1
        actual: int = self.game.get_row()
        self.assertEqual(expected, actual)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", side_effect=[0, 1])
    def test_get_row_second_try(self, mock_input):
        self.game.console.get_integer_input.side_effect = [0, 1]

        expected: int = 1
        expected_call_count: int = 2
        actual = self.game.get_row()
        actual_call_count: int = self.game.console.get_integer_input.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", side_effect=[0, 5, 6, 7, 2])
    def test_get_row_fifth_try(self, mock_input):

        expected: int = 2
        expected_call_count: int = 5
        actual = self.game.get_row()
        actual_call_count: int = self.game.console.get_integer_input.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", return_value=1)
    def test_get_col_first_try(self, mock_input):

        expected: int = 1
        actual: int = self.game.get_col()
        self.assertEqual(expected, actual)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", side_effect=[0, 1])
    def test_get_col_second_try(self, mock_input):

        expected: int = 1
        expected_call_count: int = 2
        actual = self.game.get_col()
        actual_call_count: int = self.game.console.get_integer_input.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch("Application.Utils.IOConsole.IOConsole.get_integer_input", side_effect=[0, 5, 6, 7, 2])
    def test_get_col_fifth_try(self, mock_input):

        expected: int = 2
        expected_call_count: int = 5
        actual = self.game.get_col()
        actual_call_count: int = self.game.console.get_integer_input.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch("Application.Utils.IOConsole.IOConsole.print_colored")
    def test_print_board_empty(self, mock_print):
        expected: str = ("  |   |  "
                        "\n---------\n"
                        "  |   |  "
                        "\n---------\n"
                        "  |   |  ")
        self.game.print_board()
        mock_print.assert_called_once_with(expected)

    @patch("Application.Utils.IOConsole.IOConsole.print_colored")
    def test_print_board_full(self, mock_print):
        self.game.game_board = [["x", "o", "x"],["o", "x", "o"],["x", "o", "x"]]
        expected: str = ("x | o | x"
                         "\n---------\n"
                         "o | x | o"
                         "\n---------\n"
                         "x | o | x")
        self.game.print_board()
        mock_print.assert_called_once_with(expected)

    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_row", return_value=1)
    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_col", return_value=1)
    def test_handle_turn_valid_x_turn(self, mock_col, mock_row):
        self.game.turn = 'x'
        expected_turn: str = 'o'
        expected_board: list[list[str]] = [["x", " ", " "],[" ", " ", " "],[" ", " ", " "]]

        self.assert_handle_turn(expected_turn, expected_board)

    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_row", return_value=2)
    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_col", return_value=1)
    def test_handle_turn_valid_o_turn(self, mock_col, mock_row):
        self.game.turn = 'o'
        expected_turn: str = 'x'
        expected_board: list[list[str]] = [[" ", " ", " "], ["o", " ", " "], [" ", " ", " "]]

        self.assert_handle_turn(expected_turn, expected_board)

    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_row", side_effect=[1, 2])
    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_col", side_effect=[1, 1])
    @patch("Application.Utils.IOConsole.IOConsole.print_error")
    def test_handle_turn_invalid_o_turn(self, mock_print, mock_col, mock_row):
        self.game.turn = 'o'
        self.game.game_board = [["x", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        with patch.object(self.game.console, "print_error") as mock_print:
            expected_turn: str = 'x'
            expected_board: list[list[str]] = [["x", " ", " "], ["o", " ", " "], [" ", " ", " "]]

            self.assert_handle_turn(expected_turn, expected_board)
            mock_print.assert_called_once_with("Cell already occupied")

    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_row", side_effect=[1, 2])
    @patch("Application.Casino.Games.TicTacToe.TicTacToe.TicTacToe.get_col", side_effect=[1, 1])
    def test_handle_turn_invalid_x_turn(self, mock_col, mock_row):
        self.game.turn = 'x'
        self.game.game_board = [["o", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        with patch.object(self.game.console, "print_error") as mock_print:
            expected_turn: str = 'o'
            expected_board: list[list[str]] = [["o", " ", " "], ["x", " ", " "], [" ", " ", " "]]

            self.assert_handle_turn(expected_turn, expected_board)
            mock_print.assert_called_once_with("Cell already occupied")

    def test_is_board_full_true(self):
        self.game.game_board = [
            ["x", "o", "x"],
            ["o", "x", "o"],
            ["o", "x", "o"]
        ]
        self.assertTrue(self.game.is_board_full())

    def test_is_board_full_false(self):
        self.game.game_board = [[" " for _ in range(3)]]
        self.assertFalse(self.game.is_board_full())

    def assert_handle_turn(self, expected_turn, expected_board):
        self.game.handle_turn()
        actual_turn: str = self.game.turn
        actual_board: list[list[str]] = self.game.game_board

        self.assertEqual(expected_turn, actual_turn)
        self.assertEqual(expected_board, actual_board)
