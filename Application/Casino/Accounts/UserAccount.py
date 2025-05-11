from sqlalchemy.dialects.postgresql import Any
from Application.Casino.Accounts.db import Base
from sqlalchemy import Column, String, Float, DateTime


class UserAccount(Base):

    def __init__(self, username: str, password: str, balance: float, email: str, questions: list[str], **kw: Any):
        super().__init__(**kw)
        self.username: str = username
        self.password: str = password
        self.balance: float = balance
        self.email: str = email
        self.security_question_one = questions[0]
        self.security_answer_one = questions[1]
        self.security_question_two = questions[2]
        self.security_answer_two = questions[3]

    __tablename__ = 'user_account'
    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    email = Column(String, nullable=False)
    security_question_one = Column(String, nullable=False)
    security_question_two = Column(String, nullable=False)
    security_answer_one = Column(String, nullable=False)
    security_answer_two = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiration = Column(DateTime, nullable=True)


    def subtract_losses(self, wager: float) -> None:
        if wager <= 0:
            raise ValueError("Wager must be positive")
        if wager > self.balance:
            raise ValueError(f"Insufficient funds! Available: {self.balance}, Tried to subtract: {wager}")

        self.balance -= wager

    def add_winnings(self, wager: float) -> None:
        if wager <= 0:
            raise ValueError("Wager must be positive")

        self.balance += wager

    def __repr__(self):
        return f"Username: {self.username} Balance: {self.balance}"