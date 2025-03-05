from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Event
from database.database import get_db
import datetime
import requests

router = APIRouter()

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.date >= datetime.datetime.utcnow()).all()
    return events

@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/events/add")
def add_event(event: Event, db: Session = Depends(get_db)):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# Function to Fetch Events from Alpha Vantage API
def fetch_economic_events():
    API_KEY = "DAFTY3GIV11IM6B1"
    url = f"https://www.alphavantage.co/query?function=ECONOMIC_INDICATORS&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data  # Process and insert into DB later
    else:
        return None

@router.get("/fetch-events")
def fetch_and_store_events(db: Session = Depends(get_db)):
    data = fetch_economic_events()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch events")
    
    for event in data.get("economic_events", []):
        new_event = Event(
            title=event.get("title"),
            description=event.get("description", ""),
            date=datetime.datetime.strptime(event.get("date"), "%Y-%m-%dT%H:%M:%S"),
            category="Economic",
            source_url=event.get("url", "")
        )
        db.add(new_event)
    db.commit()
    return {"message": "Events fetched and stored successfully"}
