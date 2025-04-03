from Application.Casino.Games.Game import Game


class TicTacToe(Game):
    def __init__(self, player):
        super().__init__(player)
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
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
