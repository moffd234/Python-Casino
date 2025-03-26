import csv
from Application.Casino.CasinoAccount import CasinoAccount

FP = "./accounts.csv"

def write_new_account_to_csv(account: CasinoAccount):
    account_details: list = [account.username, account.password, account.balance]

    with open(FP, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(account_details)


def read_from_csv() -> list[CasinoAccount]:
    accounts: list = []
    with open(FP, "r") as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            new_account = CasinoAccount(line[0], line[1], float(line[2]))
            accounts.append(new_account)
    return accounts


class AccountManager:
    def __init__(self):
        self.accounts: [CasinoAccount] = read_from_csv()


    def create_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username:
                return None

        return CasinoAccount(username, password)

    def register_account(self, account: CasinoAccount):
        self.accounts.append(account)
        write_new_account_to_csv(account)

    def get_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username and account.password == password:
                return account

        return None