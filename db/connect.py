from sqlalchemy import create_engine
# from configurations.settings import DB_NAME
from sqlalchemy.orm import Session

# engine = create_engine(f"sqlite:///{DB_NAME}.db",echo=False)

engine = create_engine(f"sqlite:///allme.db",echo=False)
session = Session(bind=engine)

if __name__ == "__main__":
    pass
