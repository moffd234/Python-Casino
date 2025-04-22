from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame
from Tests.BaseTest import BaseTest


class TestTriviaGame(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = UserAccount("test_username", "test_password", 50.0)
        self.game = TriviaGame(self.account, self.manager)
        self.test_question_tf = Question("is this how to spell true 'true'?", "true", ["false"])
        self.test_question_mc = Question("What is the first letter of the alphabet'?",
                                         "a", ["b", "c", "d"])

    def test_print_welcome(self):
        expected: str = r'''
        
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
        actual: str = self.game.print_welcome_message()

        self.assertEqual(expected, actual)

    def test_get_winnings_total_hard_multiple(self):
        self.game.q_type = "multiple"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 109.38
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_hard_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 87.5
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_multiple(self):

        self.game.q_type = "multiple"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 93.75
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_tf(self):

        self.game.q_type = "boolean"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 75.0
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_multiple(self):

        self.game.q_type = "multiple"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 78.12
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 62.50
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_check_answer_tf_true(self):
        self.game.score = 0
        self.game.check_answer("true", self.test_question_tf, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_right(self):
        self.game.score = 0
        self.game.check_answer("a", self.test_question_mc, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_wrong(self):
        self.game.score = 0
        self.game.check_answer("c", self.test_question_mc, 1)

        expected: int = 0
        actual = self.game.score

        self.assertEqual(expected, actual)
