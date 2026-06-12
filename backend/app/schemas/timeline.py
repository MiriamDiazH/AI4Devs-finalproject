from datetime import date
from typing import Optional
from pydantic import BaseModel


class TimelineEvent(BaseModel):
    id: str
    encounter_id: str
    category: str
    title: str
    description: str
    source_quote: str
    confidence: float
    event_date: Optional[date]


class TimelineResponse(BaseModel):
    patient_id: str
    events: list[TimelineEvent]
