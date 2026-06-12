from typing import Optional

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PatientCreate) -> Patient:
        patient = Patient(
            name=data.name,
            birth_date=data.birth_date,
            sex=data.sex,
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def list(self) -> list:
        return self.db.query(Patient).all()

    def get(self, patient_id: str) -> Optional[Patient]:
        return self.db.query(Patient).filter(Patient.id == patient_id).first()
