from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip
from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess
from Application.Casino.Games.RockPaperScissors.RPS import RPS
from Application.Casino.Games.Slots.Slots import Slots
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole
import re


def is_password_valid(password: str) -> bool:
    """
    Checks if the password has the following requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character

    :param password: password previously inputted by user
    :return: true if password is valid
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    return True if re.match(pattern, password) else False


def is_email_valid(email: str) -> bool:
    """
    Checks that the given email address has the following:
    - One or more character before an @ symbol
    - @ symbol
    - a . before a domain extension
    - Two or more characters for the domain extension after the .

    :param email: email previously inputted by user
    :return: return True if email is valid. Otherwise, returns False
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return True if re.match(pattern, email) else False


class Casino:
    def __init__(self):
        self.console = IOConsole(ANSI_COLORS.BLUE)
        self.manager = AccountManager()
        self.account: UserAccount | None = None

    def run(self) -> None:
        self.print_welcome()
        self.account: UserAccount = self.handle_initial_action()

        self.prompt_manage_or_select()

    def print_welcome(self) -> None:
        self.console.print_colored(r"""
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            
            Notes:
                - At anypoint you can exit the application by typing "exit"
                - Funds can be added and you can reset you password from the manage account screen after logging in
            """)

    def handle_login(self) -> UserAccount | None:
        for i in range(0, 5):

            username: str = self.console.get_string_input("Enter your username", return_in_lower=False)
            password: str = self.console.get_string_input("Enter your password", return_in_lower=False)

            account: UserAccount | None = self.manager.get_account(username=username, password=password)

            if account:
                return account
            else:
                self.console.print_error("Invalid username or password")

        print("Too many login attempts - returning to main screen\n\n\n")
        return None

    def handle_signup(self) -> UserAccount | None:

        while True:
            username: str = self.console.get_string_input("Create your username or type back", return_in_lower=False)

            if username == "back":
                return None

            password: str = self.console.get_string_input("Create your password", return_in_lower=False)
            email: str = self.console.get_string_input("Enter your email address", return_in_lower=False)

            if is_password_valid(password) and is_email_valid(email):
                questions_and_answers: list[str] = self.get_security_questions_and_answers()
                account: UserAccount = self.manager.create_account(username=username, password=password, email=email,
                                                                   questions=questions_and_answers)
                if account:
                    return account

                else:
                    self.console.print_error("Account with that username already exists")

            else:
                self.console.print_error("Invalid password. Password must follow the following:\n"
                                         "- At least 8 characters long\n"
                                         "- At least one uppercase letter\n"
                                         "- At least one lowercase letter\n"
                                         "- At least one number\n"
                                         "- At least one special character")

    def handle_initial_action(self) -> UserAccount:
        account: UserAccount | None = None

        while account is None:
            answer: str = self.console.get_string_input("Welcome to the Arcade Dashboard!" +
                                                        "\nFrom here, you can select any of the following options:" +
                                                        "\n\t[ signup ], [ login ]")

            if answer == "login":
                account = self.handle_login()

            elif answer == "signup":
                account = self.handle_signup()

            else:
                self.console.print_error("Invalid input. Please try again\n\n")

        return account

    def prompt_manage_or_select(self) -> None:
        while True:
            answer = self.console.get_string_input("You are logged in!" +
                                                   "\nFrom here, you can select any of the following options:" +
                                                   "\n\t[ manage-account ], [ select-game ], [ logout ]")

            if answer == "manage-account" or answer == "manage account" or answer == "manage":
                self.handle_manage_selection()

            elif answer == "select-game" or answer == "select game" or answer == "select":
                if self.account.balance < 1.00:
                    self.console.print_error("You do not have enough money to play any games")
                else:
                    self.prompt_game()
            elif answer == "logout":
                return None
            else:
                self.console.print_error("Invalid input. Please try again\n\n")

    def prompt_game(self) -> None:
        while True:
            answer = self.console.get_string_input("Welcome to the Game Selection Dashboard!" +
                                                   "\nFrom here, you can select any of the following options:" +
                                                   "\n\t[ RPS ], [ NUMBERGUESS ], [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")

            # The following are placeholders until the games are made
            if answer == "rps" or answer == "rock paper scissors":
                game = RPS(self.account, self.manager)
                game.run()

            elif answer == "numberguess" or answer == "number guess":
                game = NumberGuess(self.account, self.manager)
                game.run()

            elif answer == "trivia":
                game = TriviaGame(self.account, self.manager)
                game.run()

            elif answer == "tic-tac-toe" or answer == "tictactoe":
                game = TicTacToe(self.account, self.manager)
                game.run()

            elif answer == "coinflip" or answer == "coin flip":
                game = CoinFlip(self.account, self.manager)
                game.run()

            elif answer == "slots":
                game = Slots(self.account, self.manager)
                game.run()

            elif answer == "back":
                return None

            else:
                self.console.print_error("Invalid input. Please try again\n\n")

    def add_funds(self) -> None:
        answer: float = self.console.get_monetary_input("Enter the amount of money you want to add to your funds"
                                                        " (no less than $1.00)")
        self.manager.add_and_save_account(self.account, answer)
        self.console.print_success(f"You have added ${answer} to your funds! New Balance is {self.account.balance}")

    def reset_password(self) -> None:
        for _ in range(5):
            answer = self.console.get_string_input("Enter old password: ", return_in_lower=False)
            if answer == self.account.password:
                new_password = self.console.get_string_input("Enter new password: ", return_in_lower=False)
                self.update_password(new_password)
                return
            else:
                self.console.print_error("Passwords do not match")
        self.console.print_error("Too many invalid attempts. Please try again")

    def update_password(self, new_password) -> None:

        attempts_flag: int = 0
        while not is_password_valid(new_password) and attempts_flag < 5:
            self.console.print_error("Invalid password. Password must follow the following:\n"
                                     "- At least 8 characters long\n"
                                     "- At least one uppercase letter\n"
                                     "- At least one lowercase letter\n"
                                     "- At least one number\n"
                                     "- At least one special character")

            new_password = self.console.get_string_input("Enter new password: ", return_in_lower=False)
            attempts_flag += 1

        if attempts_flag != 5:
            self.manager.update_password(self.account, new_password)
            self.console.print_success(f"Your password has been updated!")

        else:
            self.console.print_error("Too many invalid attempts. Password was not updated.")

    def handle_manage_selection(self) -> None:
        while True:
            answer: str = self.console.get_string_input(f"You have ${self.account.balance}" +
                                                        "\nFrom here, you can select any of the following options:" +
                                                        "\n\t[ add-funds ], [reset-password], [ go-back ]")

            if answer == "add-funds" or answer == "add" or answer == "add funds":
                self.add_funds()
                return None

            elif answer == "reset-password" or answer == "reset" or answer == "reset password":
                self.reset_password()
                return None

            elif answer == "go-back" or answer == "go back" or answer == "back":
                return None

            else:
                self.console.print_error("Invalid input. Please try again")

    def get_security_question(self) -> str:
        possible_questions: list[str] = [
            "What is your favorite sports team?",
            "What street did you grow up on?",
            "What was the name of your first pet?",
            "What is your mother’s maiden name?",
            "What was the name of your elementary school?",
            "In what city were you born?",
            "What was the make of your first car?",
            "What is your favorite movie?",
            "What is your childhood best friend's first name?",
            "What was the name of your first employer?",
            "What is your favorite food?",
            "What is the name of your favorite teacher?",
            "Where did you go on your first vacation?",
            "What is the middle name of your oldest sibling?",
            "What was the name of your first stuffed animal?"
        ]

        self.console.print_colored( "Please select a security question by typing the corresponding number: ")

        for i, question in enumerate(possible_questions):
            self.console.print_colored(f"{i}. {question}")

        answer: int = self.console.get_integer_input("Your choice: ")

        while answer < 0 or answer >= len(possible_questions):
            self.console.print_error("Invalid input. Please enter a number from the list.")
            answer = self.console.get_integer_input("Your choice: ")

        return possible_questions[answer]


    def get_security_questions_and_answers(self) -> list[str]:

        first_question: str = self.get_security_question()
        first_answer: str = self.console.get_string_input(f"You selected {first_question}. Please enter your answer")

        second_question: str = self.get_security_question()
        second_answer: str = self.console.get_string_input(f"You selected {second_question}. Please enter your answer")

        return [first_question, first_answer, second_question, second_answer]