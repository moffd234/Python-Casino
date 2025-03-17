from Application.Utils.ANSI_COLORS import ANSI_COLORS


class IOConsole:
    def __init__(self, color:ANSI_COLORS=ANSI_COLORS.RED):
        if not isinstance(color, ANSI_COLORS):
            raise TypeError("color must be an instance of ANSI_COLORS")
        self.color:str = color.value

    def get_string_input(self, prompt: str, color:ANSI_COLORS=None) -> str:
        if color is None:
            color = self.color

        else:
            color = color.value

        user_input = input(color + prompt)
        if self.check_for_exit(user_input) == 1:
            exit(0)

        return user_input

    def check_for_exit(self, user_input: str) -> int:
        if user_input.lower() == "exit":
            print(self.color + "Exiting the game")
            return 1
        return 0