from Application.Utils.ANSI_COLORS import ANSI_COLORS


def count_decimals(num: float) -> int:
    str_num = str(num)
    if '.' not in str_num:
        return 0
    return len(str_num.split('.')[1])


class IOConsole:
    def __init__(self, color:ANSI_COLORS=ANSI_COLORS.GREEN):
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
                self.print_error(f"{string_response} is not a valid integer.")

    def get_float_input(self, prompt: str, color: ANSI_COLORS=None) -> float:
        while True:
            string_response: str = self.get_string_input(prompt, color)
            try:
                return float(string_response)
            except ValueError:
                self.print_error(f"{string_response} is not a valid float.")

    def get_boolean_input(self, prompt: str, color: ANSI_COLORS = None) -> bool:
        while True:
            string_response: str = self.get_string_input(prompt, color)
            string_response = string_response.strip().lower()

            if string_response in ["yes", "y", "true", "1"]:
                return True
            elif string_response in ["no", "n", "false", "0"]:
                return False
            else:
                self.print_error(f"{string_response} is not a valid boolean. Please enter yes or no.")

    def check_for_exit(self, user_input: str) -> bool:
        if user_input.lower() == "exit":
            print(self.color + "Exiting the game")
            return True
        return False

    def print_colored(self, prompt: str, color: ANSI_COLORS = None) -> None:
        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        print(color + prompt)

    def print_error(self, error_message: str) -> None:
        """
        Takes an error message and prints it in ANSI_COLORS.RED.
        :param error_message: A string value that will be printed as the error message
        :return: None
        """
        print(self.print_colored(error_message, ANSI_COLORS.RED))

    def get_monetary_input(self, prompt, color: ANSI_COLORS=None) -> float:
        """
        Prompts the user to enter a monetary amount and validates the input.
        The user will be re-prompted until a valid positive number  >= 1.00 with no more than two decimal places is entered.

        :param prompt: A string value that will be printed as the prompt
        :param color: A color from ANSI_COLORS which will be used as the printed color
        :return: A valid monetary input float
        """
        money_input: float = self.get_float_input(prompt, color)

        while count_decimals(money_input) > 2 or money_input < 1.00:
            self.print_error("Please enter a valid amount "
                             "(A positive number >= 1.00 with no more than 2 decimal places).")
            money_input = self.get_float_input(prompt, color)

        return money_input