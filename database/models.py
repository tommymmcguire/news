from sqlalchemy import Column, String, Text, DateTime
from .database import Base
import uuid

# Event Model
class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
