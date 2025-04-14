from database import Base
from sqlalchemy import Column, Integer,ForeignKey,String,Boolean,Date,Time
from sqlalchemy.orm import relationship

class Films(Base):
    __tablename__='films'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    score=Column(Integer)
    duration=Column(Integer)
    release=Column(Date)
    sessions=relationship("Sessions",back_populates="film")

class Rooms(Base):
    __tablename__="rooms"
    id=Column(Integer,primary_key=True,index=True)
    row=Column(Integer)
    column=Column(Integer)

class Sessions(Base):
    __tablename__="sessions"
    id=Column(Integer,primary_key=True,index=True)
    film_id=(Column(Integer,ForeignKey("films.id"),nullable=False))
    room_id=(Column(Integer,ForeignKey("rooms.id"),nullable=False))
    start_date=Column(Date)
    start_time=Column(Time)
    price=Column(Integer)
    expired=Column(Boolean,default=False)

    film=relationship("Films",back_populates="sessions")
    tickets = relationship("Tickets", back_populates="session")

class Tickets(Base):
    __tablename__="tickets"
    id=Column(Integer,primary_key=True,index=True)
    session_id=(Column(Integer,ForeignKey("sessions.id"),nullable=False))
    row_num=Column(Integer)
    column_num=Column(Integer)
    price=Column(Integer,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    
    
    session=relationship("Sessions",back_populates="tickets")
    user = relationship("Users", back_populates="tickets")


class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    username=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean, default=True)
    role=Column(String)
    phone_number=Column(String)

    tickets = relationship("Tickets", back_populates="user")

