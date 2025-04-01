from Application.Utils.ANSI_COLORS import ANSI_COLORS


class IOConsole:
    def __init__(self, color:ANSI_COLORS=ANSI_COLORS.RED):
        if not isinstance(color, ANSI_COLORS):
            raise TypeError("color must be an instance of ANSI_COLORS")
        self.color:str = color.value

    def get_string_input(self, prompt: str, color:ANSI_COLORS=None, return_in_lower: bool=True) -> str:
        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        user_input = input(color + prompt + "\n")
        if self.check_for_exit(user_input):
            exit(0)

        if return_in_lower:
            return user_input.lower()

        return user_input

    def get_integer_input(self, prompt: str, color:ANSI_COLORS=None) -> int:
        while True:
            string_response: str = self.get_string_input(prompt, color)
            try:
                return int(string_response)
            except ValueError:
                print(self.print_colored(f"{string_response} is not a valid integer.", ANSI_COLORS.RED))

    def get_float_input(self, prompt: str, color: ANSI_COLORS=None) -> float:
        while True:
            string_response: str = self.get_string_input(prompt, color)
            try:
                return float(string_response)
            except ValueError:
                print(self.print_colored(f"{string_response} is not a valid float.", ANSI_COLORS.RED))

    def get_boolean_input(self, prompt: str, color: ANSI_COLORS = None) -> bool:
        while True:
            string_response: str = self.get_string_input(prompt, color)
            string_response = string_response.strip().lower()

            if string_response in ["yes", "y", "true", "1"]:
                return True
            elif string_response in ["no", "n", "false", "0"]:
                return False
            else:
                print(self.print_colored(f"{string_response} is not a valid boolean. Please enter yes or no."
                                         , ANSI_COLORS.RED))

    def check_for_exit(self, user_input: str) -> bool:
        if user_input.lower() == "exit":
            print(self.color + "Exiting the game")
            return True
        return False

    def print_colored(self, prompt: str, color: ANSI_COLORS = None) -> str:
        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        return color + prompt