import requests

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Casino.Games.Game import Game
from Application.Casino.Games.TriviaGame.Category import Category
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Utils.ANSI_COLORS import ANSI_COLORS


def get_response(url) -> None | dict:
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Problem getting questions. Please try again later.")
        print(err)
        return None
    return response.json()


def create_questions(q_response: dict) -> [Question]:
    questions_list: [Question] = []
    for question in q_response["results"]:
        questions_list.append(Question(question=question["question"],
                                  answer=question["correct_answer"],
                                  wrong_answers=question["incorrect_answers"]))

    return questions_list


class TriviaGame(Game):

    def __init__(self, player: CasinoAccount):
        super().__init__(player)
        self.console.color = ANSI_COLORS.GREEN.value
        self.base_url = "https://opentdb.com/"
        self.score = 0

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


    def get_question_type(self) -> str:
        question_type: str = self.console.get_string_input("Enter the type of questions you want to play "
                                                           "(for multiple choice enter mc "
                                                           "for true or false enter tf): ")
        while question_type != "mc" and question_type != "tf":
            print(self.console.print_colored("Invalid input. Please enter either 'mc' or 'tf'", ANSI_COLORS.RED))
            question_type = self.console.get_string_input("Enter the type of questions you want to play ")

        return "boolean" if question_type == "tf" else "multiple"

    def get_difficulty(self) -> str:
        difficulty: str = self.console.get_string_input("Enter the difficulty you want to play (easy, medium, hard): ")
        while difficulty != "easy" and difficulty != "medium" and difficulty != "hard":
            print(self.console.print_colored("Invalid input. Please enter either 'easy', 'medium', or 'hard'", ANSI_COLORS.RED))
            difficulty = self.console.get_string_input("Enter the difficulty you want to play ")

        return difficulty

    def get_category(self, valid_cats: [Category]) -> Category:
        print(self.console.print_colored("Available Categories:"))
        for i in range(len(valid_cats)):
            print(self.console.print_colored(f"{i}. {valid_cats[i].name}"))

        print()

        choice = -1
        while choice < 0 or choice >= len(valid_cats):
            choice = self.console.get_integer_input("Enter category number")

            if choice < 0 or choice >= len(valid_cats):
                print(self.console.print_colored("Invalid category number", ANSI_COLORS.RED))

        return valid_cats[choice]

    def get_choices(self) -> tuple[str, str, Category]:
        q_type: str = self.get_question_type()
        difficulty: str = self.get_difficulty()

        valid_cats = self.get_valid_categories(difficulty)
        cat: Category = self.get_category(valid_cats)

        return q_type, difficulty, cat


    def get_possible_categories(self) -> list | None:
        print(self.console.print_colored("loading.........\n\n\n"))
        cat_response = get_response(f"{self.base_url}api_category.php")

        if cat_response is None:
            print("Problem getting questions. Please try again later.")
            return None

        all_categories = {category["name"]: category["id"] for category in cat_response["trivia_categories"]}
        possible_categories: list[Category] =[]

        for key, value in all_categories.items():
            response = get_response(f"{self.base_url}api_count.php?category={value}")

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

    def get_valid_categories(self, difficulty: str) -> [Category]:
        """

        Iterates through list of Categories and returns a list of only the categories that are valid

        :param difficulty: the chosen difficulty of the questions
        :return: a list of valid categories to use

        Currently, the only way to check a category's question count is the get the count of all questions. However,
        this does not specify how many of those questions are true/false and how many are multiple choice. Thus,
        we must iterate through all the possible categories and see if it has 50+ questions for a given difficulty at
        which point we can assume it has 10+ for both true/false and multiple choice
        """
        categories: [Category] = self.get_possible_categories()
        valid_categories: [Category] = []

        for cat in categories:
            if difficulty == "easy" and cat.easy_num >= 50:
                valid_categories.append(cat)

            elif difficulty == "medium" and cat.med_num >= 50:
                valid_categories.append(cat)

            elif difficulty == "hard" and cat.hard_num >= 50:
                valid_categories.append(cat)

        return valid_categories

    def check_answer(self, answer: str, question: Question) -> bool:
        if answer == question:
            self.score += 1
            return True
        else:
            return False