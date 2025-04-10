import csv
import logging
import os.path
from sqlalchemy.orm import Session

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.FeatureFlag import SQL_TRANSITION  # Feature flag for account transition to SQL
from Application.Casino.Accounts.db import SessionLocal
from Application.Casino.Accounts.CasinoAccount import CasinoAccount

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
        if SQL_TRANSITION:
            self.session: Session = SessionLocal()
        if os.path.exists("./accounts.csv"):
            self.accounts: [CasinoAccount] = read_from_csv()
        else:
            self.accounts: [CasinoAccount] = []

    def create_account(self, username: str, password: str) -> CasinoAccount | UserAccount | None:
        if SQL_TRANSITION:
            user = self.session.query(UserAccount).filter_by(username=username).first()
            if user is None:
                user = UserAccount(username, password, 50.0)
                self.session.add(user)
                self.session.commit()
                logging.debug(f"Created new user account. With username: {username}")
                return user

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

    def add_and_save_account(self, account: CasinoAccount, wager: float) -> None:
        account.add_winnings(wager)
        self.save_accounts()

    def subtract_and_save_account(self, account: CasinoAccount, wager: float) -> None:
        account.subtract_losses(wager)
        self.save_accounts()