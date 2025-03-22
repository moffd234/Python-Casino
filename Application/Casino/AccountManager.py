from Application.Casino.CasinoAccount import CasinoAccount


class AccountManager:
    def __init__(self):
        self.accounts: [CasinoAccount] = []


    def create_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username:
                return None

        return CasinoAccount(username, password)