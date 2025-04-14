from datetime import date,time
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from models import Sessions,Films,Rooms
from pydantic import BaseModel,Field


router=APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

class SessionRequest(BaseModel):
    film_id:int=Field(gt=0)
    room_id:int=Field(gt=0)
    start_date:date
    start_time:time
    price:int=Field(gt=-1)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

    



db_dependency=Annotated[Session, Depends(get_db)]


@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_active_sessions(db:db_dependency):
    return db.query(Sessions).filter(Sessions.expired==False).all()


@router.get("/read-all",status_code=status.HTTP_200_OK)
async def get_all_sessions(db:db_dependency):
    return db.query(Sessions).all()


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_session(db:db_dependency,session_request:SessionRequest):
    film=db.query(Films).filter(Films.id==session_request.film_id).first()
    if film is None:
        raise HTTPException(status_code=404,detail="film not found")
    room=db.query(Rooms).filter(Rooms.id==session_request.room_id).first()
    if room is None:
        raise HTTPException(status_code=404,detail="room not found")
    session_model=Sessions(**session_request.model_dump())
    db.add(session_model)
    db.commit()

@router.post("/change_session/{session_id}",status_code=status.HTTP_201_CREATED)
async def update_session(db:db_dependency,session_id:int,session_request:SessionRequest):
    session_model=db.query(Sessions).filter(Sessions.id==session_id).first()
    session_model.film_id=session_request.film_id
    session_model.room_id=session_request.room_id
    session_model.start_date=session_request.start_date
    session_model.start_time=session_request.start_time
    db.add(session_model)
    db.commit()

@router.delete("/delete/{session_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_session_by_id(db:db_dependency,session_id:int):
    session_model=db.query(Sessions).filter(Sessions.id==session_id).first()
    if session_model is None:
        raise HTTPException(status_code=404,detail="session not found")
    db.query(Sessions).filter(Sessions.id==session_id).first().delete()
    db.commit()


