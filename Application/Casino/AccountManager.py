import csv
from Application.Casino.CasinoAccount import CasinoAccount


def write_new_account_to_csv(account: CasinoAccount):
    account_details: list = [account.username, account.password, account.balance]

    fp = "./accounts.csv"
    with open(fp, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(account_details)

class AccountManager:
    def __init__(self):
        self.accounts: [CasinoAccount] = []


    def create_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username:
                return None

        return CasinoAccount(username, password)

    def register_account(self, account: CasinoAccount):
        self.accounts.append(CasinoAccount)
        write_new_account_to_csv(account)