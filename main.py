from fastapi import FastAPI
from routes import events
from database.database import engine
from database.models import Base

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# Include Routes
app.include_router(events.router)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
