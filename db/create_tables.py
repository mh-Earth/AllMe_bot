from models import Base
from connect import engine
import os
# os.remove('allme.db')
Base.metadata.create_all(bind=engine)