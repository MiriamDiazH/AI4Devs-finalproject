from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientResponse
from app.schemas.statewave_status import StatewaveStatusResponse
from app.services.statewave_service import StatewaveService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientResponse, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    return PatientRepository(db).create(data)


@router.get("", response_model=list[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return PatientRepository(db).list()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = PatientRepository(db).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/{patient_id}/statewave-status", response_model=StatewaveStatusResponse)
def get_patient_statewave_status(patient_id: str, db: Session = Depends(get_db)):
    """Get Statewave integration status for a patient."""
    patient = PatientRepository(db).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    status = StatewaveService().get_patient_status(patient_id)
    return StatewaveStatusResponse(**status)
