from datetime import date
from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    birth_date: date
    sex: str


class PatientResponse(BaseModel):
    id: str
    name: str
    birth_date: date
    sex: str

    model_config = {"from_attributes": True}
