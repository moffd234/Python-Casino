class IOConsole:

    def get_string_input(self, prompt: str) -> str:
        user_input = input(prompt)
        self.check_for_exit(user_input)
        return user_input

    def check_for_exit(self, user_input: str):
        if user_input.lower() == "exit":
            print("Exiting the game")
            exit(0)
