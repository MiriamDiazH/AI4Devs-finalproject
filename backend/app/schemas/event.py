from datetime import date
from typing import Optional
from pydantic import BaseModel


class ClinicalEventResponse(BaseModel):
    id: str
    encounter_id: str
    patient_id: str
    category: str
    title: str
    description: str
    source_quote: str
    confidence: float
    event_date: Optional[date]

    model_config = {"from_attributes": True}
