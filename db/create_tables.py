from models import Base
from connect import engine

import os
os.remove('sample.db')
Base.metadata.create_all(bind=engine)