from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class UserAccount(Base):
    __tablename__ = 'user_account'
    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)

    def __repr__(self):
        return f"Username: {self.username} Balance: {self.balance}"