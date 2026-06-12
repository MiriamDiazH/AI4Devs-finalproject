from datetime import date
from pydantic import BaseModel


class EncounterCreate(BaseModel):
    patient_id: str
    date: date
    type: str
    note_text: str


class EncounterResponse(BaseModel):
    id: str
    patient_id: str
    date: date
    type: str
    note_text: str

    model_config = {"from_attributes": True}
