from sqlalchemy import engine,String,Integer,Column,Boolean,create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
# from CommandMaker.model import Command
import sys

engine = create_engine("sqlite:///")
# print(sys.path())

from CommandMaker.model import Trackinsta

Base = declarative_base()


    
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)


    # trackinsta = Command(commandName="Trackinsta",commandDes="Track instagram id")
    # session.add(trackinsta)

    # commandList = CommandList(commandId=trackinsta.commandId,commandName=trackinsta.commandName)
    # session.add(commandList)

    user1 = Trackinsta("emi_lyitachi","itachi",20,32,True,"",)
    user2 = Trackinsta("blackpinkofficial","black",222233235,4,False,"")
    user3 = Trackinsta("afnan.aksa","Afnan Aksa",1,1,False,"")

    # session.add(user1)
    # session.add(user2)
    # session.add(user3)

    # session.commit()
    # allQuery = session.query(Trackinsta).filter_by(username='afnan.aksa')


    