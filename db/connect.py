from sqlalchemy import create_engine
from configurations.settings import DATABASE_NAME,DATABASE_HOST,DATABASE_PASSWORD,DATABASE_USERNAME
from sqlalchemy.orm import Session

# engine = create_engine(f"sqlite:///{DB_NAME}.db",echo=False)

# engine = create_engine(f"mysql+pymysql://",echo=False)
engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}",echo=False)


# server='DESKTOP-G24QTHH\SQLEXPRESS'
# driver='ODBC+Driver+17+for+SQL+Server'
# database='master'
# connection = f'mssql://@{server}/{database}?driver={driver}'

# engine = create_engine(connection,echo=False)

session = Session(bind=engine)

if __name__ == "__main__":
    pass
