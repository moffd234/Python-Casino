import requests

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Casino.Games.Game import Game


class TriviaGame(Game):

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

    def __init__(self, player: CasinoAccount):
        super().__init__(player)

    def get_response(self, url) -> None | dict:
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Problem getting questions. Please try again later.")
            return None
        return response.json()