from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from models import Rooms
from pydantic import BaseModel,Field


router=APIRouter(
    prefix="/rooms",
    tags=['rooms']
)
class RoomRequest(BaseModel):
    row:int=Field(gt=0)
    column:int=Field(gt=0)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_rooms(db:db_dependency):
    return db.query(Rooms).all()

@router.post("/add-room",status_code=status.HTTP_201_CREATED)
async def create_film(db:db_dependency,room_request:RoomRequest):
    film_model=Rooms(**room_request.model_dump())
    db.add(film_model)
    db.commit()

@router.get("/get-room-by-id/{room_id}",status_code=status.HTTP_200_OK)
async def get_room_by_id(db:db_dependency,room_id:int):
    room=db.query(Rooms).filter(Rooms.id==room_id).first()
    if room is None:
        raise HTTPException(status_code=404,detail="room not found")
    return room

@router.post("/edit-room/{room_id}")
async def update_room_by_id(db:db_dependency,room_id:int,room_request:RoomRequest):
    room_model=db.query(Rooms).filter(Rooms.id==room_id).first()
    if room_model is None:
        raise HTTPException(status_code=404,detail="room not found")
    room_model.column=room_request.column
    room_model.row=room_request.row
    db.add(room_model)
    db.commit()

@router.get("/delete-room/{room_id}")
async def delete_room_by_id(db:db_dependency,room_id:int):
    room_model=db.query(Rooms).filter(Rooms.id==room_id).first()
    if room_model is None:
        raise HTTPException(status_code=404,detail="room not found")
    db.query(Rooms).filter(Rooms.id==room_id).delete()
    db.commit()
###delete room
###update room