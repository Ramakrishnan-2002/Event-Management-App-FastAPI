from .database import Base
from sqlalchemy import String,Integer,Column,TIMESTAMP,func,Date,Time

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False,unique=True)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())


class Event(Base):
    __tablename__="events"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    startDate=Column(Date,nullable=False)
    startTime=Column(Time,nullable=False)
    endDate=Column(Date,nullable=False)
    endTime=Column(Time,nullable=False)
    created_by=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())