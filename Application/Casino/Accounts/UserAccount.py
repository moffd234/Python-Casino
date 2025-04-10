from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()

class UserAccount(Base):

    def __init__(self, username, password, balance, **kw: Any):
        super().__init__(**kw)
        self.username = username
        self.password = password
        self.balance = balance

    __tablename__ = 'user_account'
    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)

    def __repr__(self):
        return f"Username: {self.username} Balance: {self.balance}"