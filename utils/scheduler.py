from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import SessionLocal
from models import Sessions

def update_expired_sessions():
    db=SessionLocal()
    try:
        sessions=db.query(Sessions).filter(Sessions.expired==False).all()
        for session in sessions:
            sessions_datetime=datetime.combine(session.start_date,session.start_time)
            if datetime.now()>sessions_datetime:
                session.expired=True
                db.add(session)
        db.commit()
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(update_expired_sessions, 'interval', minutes=1)