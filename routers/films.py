import datetime
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from models import Films
from pydantic import BaseModel,Field


router=APIRouter(
    prefix="/films",
    tags=['films']
)

class FilmRequest(BaseModel):
    title: str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    duration:int = Field(gt=0,lt=300)
    release:datetime.date
    score:int =Field(gt=0,lt=11)
    model_config = {
        "arbitrary_types_allowed": True  
    }


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Films).all()

@router.post("/add-film",status_code=status.HTTP_201_CREATED)
async def create_film(db:db_dependency,film_request:FilmRequest):
    film_model=Films(**film_request.model_dump())
    db.add(film_model)
    db.commit()

@router.get("/{film_name}",status_code=status.HTTP_200_OK)
async def filter_films_by_name(film_name:str,db:db_dependency):
    films=db.query(Films).filter(Films.title.ilike(f"%{film_name}%")).all()
    if films is None:
        raise HTTPException(status_code=404,detail="film not found")
    return films

@router.get("/score/{film_score}",status_code=status.HTTP_200_OK)
async def filter_films_by_name(film_score:int,db:db_dependency):
    films=db.query(Films).filter(Films.score>=film_score).all()
    if films is None:
        raise HTTPException(status_code=404,detail="film not found")
    return films

@router.post("/change-film/{film_id}",status_code=status.HTTP_204_NO_CONTENT)
async def change_film_description(film_id:int,db:db_dependency,film_request:FilmRequest):
    film=db.query(Films).filter(Films.id==film_id).first()
    if film is None:
        raise HTTPException(status_code=404,detail="film not found")
    film.description=film_request.description
    film.title=film_request.title
    film.score=film_request.score
    film.release=film_request.release
    film.duration=film_request.release
    db.add(film)
    db.commit()

@router.delete("/delete-film/{film_id}")
async def delete_film_by_id(db:db_dependency,film_id:int):
    film_model=db.query(Films).filter(Films.id==film_id).first()
    if film_model is None:
        raise HTTPException(status_code=404,detail="film not found")
    db.query(Films).filter(Films.id==film_id).delete()
    db.commit()