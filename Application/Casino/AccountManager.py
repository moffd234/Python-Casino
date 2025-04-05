import csv
import logging
import os.path

from Application.Casino.CasinoAccount import CasinoAccount

FP = "./accounts.csv"

def write_new_account_to_csv(account: CasinoAccount) -> None:
    account_details: list = [account.username, account.password, account.balance]

    try:
        with open(FP, "a", newline='') as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(account_details)

    except FileNotFoundError:
        with open(FP, "w", newline='') as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(account_details)
    logging.debug("Wrote new account to file.")

def read_from_csv() -> list[CasinoAccount]:
    accounts: list = []
    with open(FP, "r") as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            new_account = CasinoAccount(line[0], line[1], float(line[2]))
            accounts.append(new_account)
    logging.debug("Read all accounts from file.")
    return accounts


class AccountManager:
    def __init__(self):
        if os.path.exists("./accounts.csv"):
            self.accounts: [CasinoAccount] = read_from_csv()
        else:
            self.accounts: [CasinoAccount] = []

    def create_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username:
                return None

        return CasinoAccount(username, password)

    def register_account(self, account: CasinoAccount) -> None:
        self.accounts.append(account)
        write_new_account_to_csv(account)

    def get_account(self, username: str, password: str) -> CasinoAccount | None:
        for account in self.accounts:
            if account.username == username and account.password == password:
                return account

        return None

    def save_accounts(self) -> None:
        with open(FP, "w", newline='') as file:
            writer = csv.writer(file, lineterminator="\n")
            for account in self.accounts:
                writer.writerow([account.username, account.password, account.balance])
        logging.debug("Saved all accounts to file.")