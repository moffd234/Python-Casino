from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Application.Casino.Accounts.UserAccount import Base

engine = create_engine('sqlite:///casino.db', echo=False)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
