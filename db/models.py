from sqlalchemy.orm import Mapped,DeclarativeBase,mapped_column,relationship
from sqlalchemy import ForeignKey,Text,String,Integer,Boolean,Float,BigInteger,Unicode
from typing import Any, List,Optional
import uuid
import time
import datetime

def gen_uuid():
    return str(uuid.uuid4())

def create_at():
    return datetime.datetime.utcnow()
class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = 'users'
    user_id:Mapped[int] = mapped_column(BigInteger,primary_key=True)
    telegram_username:Mapped[str] = mapped_column(String(64),nullable=True)
    first_name:Mapped[str] = mapped_column(String(64),nullable=True)
    last_name:Mapped[str] = mapped_column(String(64),nullable=True)
    active_tracker:Mapped[int] = mapped_column(Integer,nullable=True)
    trackers:Mapped[List["Trackers"]] = relationship(back_populates='trackers')


    def __init__(self,username:str,user_id:int,first:str,last:str,trackers:list['Trackers'],active_tracker:int=-1, **kw: Any):
    
        super().__init__(**kw)
        self.user_id = user_id
        self.telegram_username = username
        self.first_name = first
        self.last_name = last
        self.trackers = trackers
        self.active_tracker = active_tracker

    def __repr__(self) -> str:
        return f"<User username = {self.first_name}, user_id = {self.user_id}>"

class Trackers(Base):
    __tablename__ = 'trackers'
    user_id:Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'),primary_key=True)
    tracker_name:Mapped[str] = mapped_column(String(64),primary_key=True, nullable=False)
    initial_data:Mapped[str] = mapped_column(String(64),nullable=False)
    continues_data:Mapped[str] = mapped_column(Text,nullable=True)
    total_data:Mapped[int] = mapped_column(Integer,default=1)

    trackers:Mapped["User"] = relationship(back_populates='trackers')


    
    def __init__(self,tracker_name:str,initial_data:str,continues_data=None,user_id=None, **kw: Any):
        super().__init__(**kw)
        self.tracker_name = tracker_name
        self.initial_data = initial_data
        self.continues_data = continues_data
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<Tracker user_id={self.user_id}, tracker_name={self.tracker_name}>"


class TrackinstaData(Base):

    __tablename__ = 'trackinstadata'
    uid:Mapped[uuid.UUID] = mapped_column(String(64), primary_key=True)
    username:Mapped[str] = mapped_column(String(64),nullable=False)
    follower:Mapped[int] = mapped_column(Integer,nullable=False)
    following:Mapped[int] = mapped_column(Integer,nullable=False)
    isPrivate:Mapped[bool] = mapped_column(Boolean,nullable=False)
    verified:Mapped[bool] = mapped_column(Boolean,nullable=False)
    full_name:Mapped[Optional[str]] = mapped_column(Unicode(length=64))
    bio:Mapped[Optional[str]] = mapped_column(Unicode(length=200))
    dp:Mapped[Optional[str]] = mapped_column(Text)
    timestamp:Mapped[float] = mapped_column(Float,default=time.time)


    # tracker:Mapped[str] = mapped_column(String(64),ForeignKey('trackinsta.tracker'))

    def __init__(self,uid:str,username:str,follower:int,following:int,isPrivate:bool,verified:bool,full_name:str|None=None,bio:str|None=None,dp:str|None=None,timestamp:float=None,**kw: Any):
        super().__init__(**kw)
        self.uid = uid
        self.username = username
        self.full_name = full_name
        self.follower = follower
        self.following = following
        self.isPrivate = isPrivate
        self.verified = verified
        self.bio = bio
        self.dp = dp
        self.timestamp = timestamp
