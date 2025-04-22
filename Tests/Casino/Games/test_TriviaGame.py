from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame, create_questions
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

    def test_create_questions_mc(self):
        response = {'response_code': 0, 'results': [
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'The Porygon Line',
             'difficulty': 'easy', 'incorrect_answers': ['The Pikachu Line', 'The Elekid Line', 'The Magby Line'],
             'question': 'Which Pok&eacute;mon and it&#039;s evolutions were banned from appearing in a main role after the Episode 38 Incident?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Caterpie',
             'difficulty': 'easy', 'incorrect_answers': ['Charmander', 'Pikachu', 'Pidgey'],
             'question': 'What was Ash Ketchum&#039;s second Pokemon?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'God', 'difficulty': 'easy',
             'incorrect_answers': ['Alien', 'Time Traveler', 'Esper'],
             'question': 'In &quot;The Melancholy of Haruhi Suzumiya&quot; series, the SOS Brigade club leader is unknowingly treated as a(n) __ by her peers.',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Manaphy', 'difficulty': 'easy',
             'incorrect_answers': ['Ash', 'May', 'Phantom'],
             'question': 'In the 9th Pokemon movie, who is the Prince of the Sea?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Sen (Thousand)',
             'difficulty': 'easy', 'incorrect_answers': ['Hyaku (Hundred)', 'Ichiman (Ten thousand)', 'Juu (Ten)'],
             'question': 'What name is the main character Chihiro given in the 2001 movie &quot;Spirited Away&quot;?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Elizabeth Midford',
             'difficulty': 'easy',
             'incorrect_answers': ['Rachel Phantomhive', 'Alexis Leon Midford', 'Angelina Dalles'],
             'question': 'In the anime Black Butler, who is betrothed to be married to Ciel Phantomhive?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Gainax', 'difficulty': 'easy',
             'incorrect_answers': ['Kyoto Animation', 'Pierrot', 'A-1 Pictures'],
             'question': 'What animation studio produced &quot;Gurren Lagann&quot;?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': '8+', 'difficulty': 'easy',
             'incorrect_answers': ['6+', '4+', '5+'],
             'question': 'How many &quot;JoJos&quot; that are protagonists are there in the series &quot;Jojo&#039;s Bizarre Adventure&quot;?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Kaname Chidori',
             'difficulty': 'easy', 'incorrect_answers': ['Teletha Testarossa', 'Melissa Mao', 'Kyoko Tokiwa'],
             'question': 'Who is the main heroine of the anime, Full Metal Panic!', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Reiner Braun',
             'difficulty': 'easy', 'incorrect_answers': ['Armin Arlelt', 'Mikasa Ackermann', 'Eren Jaeger'],
             'question': 'Who is the armored titan in &quot;Attack On Titan&quot;?', 'type': 'multiple'}]}
        expected_list: list[Question] = [Question(
            question="Which Pokémon and it's evolutions were banned from appearing in a main role after the Episode 38 Incident?",
            answer="The Porygon Line",
            wrong_answers=["The Pikachu Line", "The Elekid Line", "The Magby Line"]),
            Question(
                question="What was Ash Ketchum's second Pokemon?",
                answer="Caterpie",
                wrong_answers=["Charmander", "Pikachu", "Pidgey"]),
            Question(
                question='In "The Melancholy of Haruhi Suzumiya" series, the SOS Brigade club leader is unknowingly treated as a(n) __ by her peers.',
                answer="God",
                wrong_answers=["Alien", "Time Traveler", "Esper"]),
            Question(
                question="In the 9th Pokemon movie, who is the Prince of the Sea?",
                answer="Manaphy",
                wrong_answers=["Ash", "May", "Phantom"]),
            Question(
                question='What name is the main character Chihiro given in the 2001 movie "Spirited Away"?',
                answer="Sen (Thousand)",
                wrong_answers=["Hyaku (Hundred)", "Ichiman (Ten thousand)", "Juu (Ten)"]
            ),
            Question(
                question="In the anime Black Butler, who is betrothed to be married to Ciel Phantomhive?",
                answer="Elizabeth Midford",
                wrong_answers=["Rachel Phantomhive", "Alexis Leon Midford", "Angelina Dalles"]
            ),
            Question(
                question='What animation studio produced "Gurren Lagann"?',
                answer="Gainax",
                wrong_answers=["Kyoto Animation", "Pierrot", "A-1 Pictures"]
            ),
            Question(
                question='How many "JoJos" that are protagonists are there in the series "Jojo\'s Bizarre Adventure"?',
                answer="8+",
                wrong_answers=["6+", "4+", "5+"]
            ),
            Question(
                question="Who is the main heroine of the anime, Full Metal Panic!",
                answer="Kaname Chidori",
                wrong_answers=["Teletha Testarossa", "Melissa Mao", "Kyoko Tokiwa"]
            ),
            Question(
                question='Who is the armored titan in "Attack On Titan"?',
                answer="Reiner Braun",
                wrong_answers=["Armin Arlelt", "Mikasa Ackermann", "Eren Jaeger"]
            )
        ]
        self.assert_create_questions(expected_list, response)

    def test_create_questions_tf(self):
        response = {'response_code': 0, 'results': [
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'Brandon Routh plays the titular character in the movie &quot;John Wick&quot;.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
                                  'incorrect_answers': ['False'],
                                  'question': 'Samuel L. Jackson had the words, &#039;Bad Motherf*cker&#039; in-scripted on his lightsaber during the filming of Star Wars.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'],
             'question': 'In the original Star Wars trilogy, David Prowse was the actor who physically portrayed Darth Vader.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
                                  'incorrect_answers': ['True'],
                                  'question': 'Leonardo DiCaprio won an Oscar for Best Actor in 2004&#039;s &quot;The Aviator&quot;.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'Shaquille O&#039;Neal appeared in the 1997 film &quot;Space Jam&quot;.', 'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'],
             'question': 'In the original script of &quot;The Matrix&quot;, the machines used humans as additional computing power instead of batteries.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
                                  'incorrect_answers': ['True'],
                                  'question': 'Han Solo&#039;s co-pilot and best friend, &quot;Chewbacca&quot;, is an Ewok.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'], 'question': 'Actor Tommy Chong served prison time.', 'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'The 2010 film &quot;The Social Network&quot; is a biographical drama film about MySpace founder Tom Anderson.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
                                  'incorrect_answers': ['False'],
                                  'question': 'The movie &quot;The Nightmare before Christmas&quot; was all done with physical objects.',
                                  'type': 'boolean'}]}
        expected_list: list[Question] = [Question(
            question='Brandon Routh plays the titular character in the movie "John Wick".',
            answer='False',
            wrong_answers=['True']
        ),
            Question(
                question="Samuel L. Jackson had the words, 'Bad Motherf*cker' in-scripted on his lightsaber during the filming of Star Wars.",
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='In the original Star Wars trilogy, David Prowse was the actor who physically portrayed Darth Vader.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='Leonardo DiCaprio won an Oscar for Best Actor in 2004\'s "The Aviator".',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='Shaquille O\'Neal appeared in the 1997 film "Space Jam".',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='In the original script of "The Matrix", the machines used humans as additional computing power instead of batteries.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='Han Solo\'s co-pilot and best friend, "Chewbacca", is an Ewok.',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='Actor Tommy Chong served prison time.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='The 2010 film "The Social Network" is a biographical drama film about MySpace founder Tom Anderson.',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='The movie "The Nightmare before Christmas" was all done with physical objects.',
                answer='True',
                wrong_answers=['False']
            )
        ]
        self.assert_create_questions(expected_list, response)

    def assert_create_questions(self, expected_list, response):
        expected_length: int = len(expected_list)
        actual_list: list[Question] = create_questions(response)
        actual_length: int = len(actual_list)

        for i in range(len(expected_list)):
            self.assertEqual(expected_list[i].question, actual_list[i].question)
            self.assertEqual(expected_list[i].answer, actual_list[i].answer)
            self.assertEqual(expected_list[i].wrong_answers, actual_list[i].wrong_answers)
            self.assertEqual(expected_length, actual_length)