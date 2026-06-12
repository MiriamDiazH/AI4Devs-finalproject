from sqlalchemy.orm import Session

from app.models.clinical_event import ClinicalEvent


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bulk(self, events: list[ClinicalEvent]) -> list[ClinicalEvent]:
        self.db.add_all(events)
        self.db.commit()
        for e in events:
            self.db.refresh(e)
        return events

    def list_by_patient(self, patient_id: str) -> list[ClinicalEvent]:
        return (
            self.db.query(ClinicalEvent)
            .filter(ClinicalEvent.patient_id == patient_id)
            .order_by(ClinicalEvent.event_date)
            .all()
        )
