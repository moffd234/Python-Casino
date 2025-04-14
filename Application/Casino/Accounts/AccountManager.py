import logging
from typing import Optional
from sqlalchemy.orm import Session

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Accounts.db import init_db


class AccountManager:
    def __init__(self, session=None):
        self.session: Session = session or init_db()

    def create_account(self, username: str, password: str) -> UserAccount | None:
        user: Optional[UserAccount] = self.session.query(UserAccount).filter_by(username=username).first()

        if user:
            return None

        user = UserAccount(username, password, 50.0)
        self.session.add(user)
        self.session.commit()
        logging.debug(f"Created new user account. With username: {username}")
        return user

    def get_account(self, username: str, password: str) -> UserAccount | None:
        user: Optional[UserAccount] = self.session.query(UserAccount).filter_by(username=username).first()

        if user is not None and user.password == password:
            return user

        return None

    def add_and_save_account(self, account: UserAccount, wager: float) -> None:
        account.add_winnings(wager)
        self.session.commit()

    def subtract_and_save_account(self, account: UserAccount, wager: float) -> None:
        account.subtract_losses(wager)
        self.session.commit()

    def update_password(self, account: UserAccount, new_password: str) -> None:
        account.password = new_password
        self.session.commit()
