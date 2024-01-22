from models import Base
from connect import engine
import os

Base.metadata.create_all(bind=engine)