from sqlalchemy import engine,String,Integer,Column,Boolean,create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import uuid


engine = create_engine("sqlite:///")


Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Admin(Base):
    __tablename__ = 'Admins'

    Name = Column('name',String)
    User_id = Column('user_id',Integer,primary_key=True)


    def __init__(self,name,user_id):
        self.Name = name
        self.User_id = user_id


class Command(Base):
    __tablename__ = "Commands"

    Id = Column('Id',String,primary_key=True,default=generate_uuid)
    commandName = Column("CommandName" ,String)
    commandDes = Column("CommandDescription" ,String)


    def __init__(self,commandName,commandDes):
        self.commandName = commandName
        self.commandDes = commandDes


class Resister():
    def __init__(self, commandName, commandDes):
        super().__init__(commandName, commandDes)
        

    
if __name__ == "__main__":
    ...

    