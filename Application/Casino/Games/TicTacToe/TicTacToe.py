from Application.Casino.Games.Game import Game
from Application.Utils.ANSI_COLORS import ANSI_COLORS


class TicTacToe(Game):
    def __init__(self, player):
        super().__init__(player)
        self.game_board: list[list[str]] = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "x"

    def print_welcome_message(self) -> str:
        pass

    def run(self):
        pass

    def print_board(self) -> None:
        board_lines = []
        for row in self.game_board:
            board_lines.append(" | ".join(row))
        board_display = "\n---------\n".join(board_lines)
        print(self.console.print_colored(board_display))

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.game_board[row][col] == " "

    def get_row(self) -> int:
         row = self.console.get_integer_input("Enter row number (1-3)")

         while row < 1 or row > 3:
             print(self.console.print_colored("Row number must be between 1 and 3", ANSI_COLORS.RED))
             row = self.console.get_integer_input("Enter row number (1-3)")

         return row

    def get_col(self) -> int:
        col = self.console.get_integer_input("Enter column number (1-3)")

        while col < 1 or col > 3 or not self.is_cell_empty(col - 1, 0):
            print(self.console.print_colored("Column number must be between 1 and 3", ANSI_COLORS.RED))
            col = self.console.get_integer_input("Enter column number (1-3)")

        return col

    def handle_turn(self) -> None:
        row = self.get_row()
        col = self.get_col()

        while not self.is_cell_empty(row - 1, col - 1):
            print(self.console.print_colored("Cell already occupied", ANSI_COLORS.RED))
            row = self.get_row()

        self.game_board[row - 1][col - 1] = self.turn