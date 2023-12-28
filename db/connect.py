from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///sample.db",echo=False)
session = Session(bind=engine)

if __name__ == "__main__":
    pass
