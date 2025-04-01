import requests

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Casino.Games.Game import Game
from Application.Casino.Games.TriviaGame.Category import Category
from Application.Utils.ANSI_COLORS import ANSI_COLORS


class TriviaGame(Game):

    def __init__(self, player: CasinoAccount):
        super().__init__(player)
        self.console.color = ANSI_COLORS.GREEN.value
        self.base_url = "https://opentdb.com/"

    def print_welcome_message(self) -> str:
        return r'''
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      888888 88""Yb 88 Yb    dP 88    db    
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb       88   88__dP 88  Yb  dP  88   dPYb   
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP       88   88"Yb  88   YbdP   88  dP__Yb  
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP        88   88  Yb 88    YP    88 dP""""Yb 
        
        Rules:
                1. Select difficulty, category, and the type of questions 
                  -Payout is:
                             1.25x your wager if you choose medium
                             1.5x your wager if you choose hard
                             an additional 1.25x your wager if you choose multiple choice
                2. You will then be given 10 questions from that category
                3. You must answer at least 7 questions correctly to win
        '''

    def run(self):
        pass

    def get_response(self, url) -> None | dict:
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Problem getting questions. Please try again later.")
            return None
        return response.json()

    def get_question_type(self) -> str:
        question_type: str = self.console.get_string_input("Enter the type of questions you want to play "
                                                           "(for multiple choice enter mc "
                                                           "for true or false enter tf): ")
        while question_type != "mc" and question_type != "tf":
            print(self.console.print_colored("Invalid input. Please enter either 'mc' or 'tf'", ANSI_COLORS.RED))
            question_type = self.console.get_string_input("Enter the type of questions you want to play ")

        return question_type

    def get_difficulty(self) -> str:
        difficulty: str = self.console.get_string_input("Enter the difficulty you want to play (easy, medium, hard): ")
        while difficulty != "easy" and difficulty != "medium" and difficulty != "hard":
            print(self.console.print_colored("Invalid input. Please enter either 'easy', 'medium', or 'hard'", ANSI_COLORS.RED))
            difficulty = self.console.get_string_input("Enter the difficulty you want to play ")

        return difficulty

    def get_possible_categories(self) -> list | None:
        cat_response = self.get_response(f"{self.base_url}api_category.php")

        if cat_response is None:
            print("Problem getting questions. Please try again later.")
            return None

        all_categories = {category["name"]: category["id"] for category in cat_response["trivia_categories"]}
        possible_categories: list[Category] =[]

        for key, value in all_categories.items():
            response = self.get_response(f"{self.base_url}api_count.php?category={value}")

            if response:
                category_data = response.get("category_question_count", {})
                possible_categories.append(Category(
                    name=key,
                    id_num=value,
                    easy_num=category_data.get("total_easy_question_count", 0),
                    med_num=category_data.get("total_medium_question_count", 0),
                    hard_num=category_data.get("total_hard_question_count", 0)
                ))

        return possible_categories