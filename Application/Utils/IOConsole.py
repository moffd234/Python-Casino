from Application.Utils.ANSI_COLORS import ANSI_COLORS


class IOConsole:
    def __init__(self, color=ANSI_COLORS.RED):
        self.color:str = color

    def get_string_input(self, prompt: str) -> str:
        user_input = input(prompt)
        self.check_for_exit(user_input)
        return user_input

    def check_for_exit(self, user_input: str):
        if user_input.lower() == "exit":
            print(self.color + "Exiting the game" + ANSI_COLORS.RESET)
            exit(0)

