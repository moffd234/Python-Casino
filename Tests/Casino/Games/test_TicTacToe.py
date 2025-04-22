from unittest.mock import patch
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe
from Tests.BaseTest import BaseTest

class TestTicTacToe(BaseTest):

    def setUp(self):
        super().setUp()
        self.game = TicTacToe(self.manager.get_account("Username", "Password"), self.manager)

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