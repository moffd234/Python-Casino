from Application.Casino.Games.Game import Game


class RPS(Game):
    def print_welcome_message(self) -> str:
        pass

    def run(self):
        pass

    def __init__(self, player, manager):
        super().__init__(player, manager)


    def get_turn(self) -> str:
        turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        while turn != "Rock" and turn != "Paper" and turn != "Scissors":
            turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        return turn