from fastapi import FastAPI,status
import models
from database import engine
from routers import films,rooms,session
from utils.scheduler import scheduler



app=FastAPI()

@app.on_event("startup")
def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

models.Base.metadata.create_all(bind=engine)

app.include_router(films.router)
app.include_router(rooms.router)
app.include_router(session.router)