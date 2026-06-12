from typing import Optional

from sqlalchemy.orm import Session

from app.models.encounter import Encounter
from app.schemas.encounter import EncounterCreate


class EncounterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: EncounterCreate) -> Encounter:
        encounter = Encounter(
            patient_id=data.patient_id,
            date=data.date,
            type=data.type,
            note_text=data.note_text,
        )
        self.db.add(encounter)
        self.db.commit()
        self.db.refresh(encounter)
        return encounter

    def list_by_patient(self, patient_id: str) -> list:
        return (
            self.db.query(Encounter)
            .filter(Encounter.patient_id == patient_id)
            .all()
        )

    def get(self, encounter_id: str) -> Optional[Encounter]:
        return self.db.query(Encounter).filter(Encounter.id == encounter_id).first()
