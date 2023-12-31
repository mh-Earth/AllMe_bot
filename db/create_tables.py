from models import Base
from connect import engine
import os
# os.remove(DB_NAME)
os.remove('allme.db')
Base.metadata.create_all(bind=engine)