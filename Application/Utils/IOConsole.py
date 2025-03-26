from Application.Utils.ANSI_COLORS import ANSI_COLORS


class IOConsole:
    def __init__(self, color:ANSI_COLORS=ANSI_COLORS.RED):
        if not isinstance(color, ANSI_COLORS):
            raise TypeError("color must be an instance of ANSI_COLORS")
        self.color:str = color.value

    def get_string_input(self, prompt: str, color:ANSI_COLORS=None) -> str:
        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        user_input = input(color + prompt + "\n")
        if self.check_for_exit(user_input):
            exit(0)

        return user_input

    def get_integer_input(self, prompt: str, color:ANSI_COLORS=None):
        string_response: str = self.get_string_input(prompt, color)
        try:
            return int(string_response)
        except ValueError:
            print(f"{string_response} is not a valid integer.")
            return self.get_integer_input(prompt, color)

    def get_float_input(self, prompt: str, color: ANSI_COLORS=None):
        string_response: str = self.get_string_input(prompt, color)
        try:
            return float(string_response)
        except ValueError:
            print(f"{string_response} is not a valid float.")


    def check_for_exit(self, user_input: str) -> bool:
        if user_input.lower() == "exit":
            print(self.color + "Exiting the game")
            return True
        return False
