import requests

from Application.Casino.CasinoAccount import CasinoAccount
from Application.Casino.Games.Game import Game


class TriviaGame(Game):

    def print_welcome_message(self) -> str:
        pass

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