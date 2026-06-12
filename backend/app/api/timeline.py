from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.patient_repository import PatientRepository
from app.repositories.event_repository import EventRepository
from app.schemas.timeline import TimelineEvent, TimelineResponse

router = APIRouter(prefix="/patients", tags=["timeline"])


@router.get("/{patient_id}/timeline", response_model=TimelineResponse)
def get_timeline(patient_id: str, db: Session = Depends(get_db)):
    patient = PatientRepository(db).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    events = EventRepository(db).list_by_patient(patient_id)
    return TimelineResponse(
        patient_id=patient_id,
        events=[
            TimelineEvent(
                id=e.id,
                encounter_id=e.encounter_id,
                category=e.category,
                title=e.title,
                description=e.description,
                source_quote=e.source_quote,
                confidence=e.confidence,
                event_date=e.event_date,
            )
            for e in events
        ],
    )
