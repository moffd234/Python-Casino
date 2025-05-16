import datetime
import logging
import smtplib
from typing import Optional
from sqlalchemy.orm import Session
import uuid

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Accounts.db import init_db

class AccountManager:
    def __init__(self, session=None):
        self.session: Session = session or init_db()

    def create_account(self, username: str, password: str, email: str, questions: list[str]) -> UserAccount | None:
        """
        Attempts to create a new user account with the provided credentials and security questions.

        Checks if a user with the given username already exists in the database. If the username is unique, a new
        UserAccount is created with a default balance of $50.00, added to the session, and committed to the database.

        Args:
            username (str): The desired username for the new account.
            password (str): The password associated with the account.
            email (str): The email address tied to the account for recovery or contact purposes.
            questions (list[str]): A list of security questions for account recovery.

        Returns:
                UserAccount | None: The newly created UserAccount object if successful, or None if the username is already taken.
        """
        user: Optional[UserAccount] = self.session.query(UserAccount).filter_by(username=username).first()

        if user:
            return None

        user = UserAccount(username, password, 50.0, email, questions)
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

    def generate_uuid_and_store_it(self, account: UserAccount) -> str:
        token: uuid = uuid.uuid4()
        token_expiration: datetime = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        account.reset_token = token
        account.reset_token_expiration = token_expiration

        self.session.commit()
        return str(token)

    def invalidate_reset_token(self, account: UserAccount):
        account.reset_token = None
        account.reset_token_expiration = None
        self.session.commit()

    def email_recovery_token(self, account: UserAccount) -> None:
        from os import getenv
        from dotenv import load_dotenv, find_dotenv

        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        username: str = getenv("G_USERNAME")
        password: str = getenv("G_KEY")

        token: str = self.generate_uuid_and_store_it(account)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(username, password)
            subject: str = "Python Casino Password Reset"
            body: str = (f"Below is your password reset token.\n"
                         f"Please paste it in the prompt on the application:\n\n{token}")
            message = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(username, account.email, message)