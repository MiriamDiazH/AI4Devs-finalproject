from __future__ import annotations

from datetime import date

from sqlalchemy import select

from app.core.database import Base, SessionLocal, engine
from app.models.clinical_event import ClinicalEvent
from app.models.encounter import Encounter
from app.models.patient import Patient

SEED_DATA = [
    {
        "patient": {
            "name": "Laura Benitez",
            "birth_date": date(1981, 4, 17),
            "sex": "F",
        },
        "encounters": [
            {
                "date": date(2026, 2, 11),
                "type": "Atencion primaria",
                "note_text": "Refiere cefalea frecuente y cansancio. TA 150/95. Se solicita analitica.",
                "events": [
                    {
                        "category": "symptom",
                        "title": "Cefalea recurrente",
                        "description": "Dolor de cabeza de varias semanas.",
                        "source_quote": "Refiere cefalea frecuente y cansancio.",
                        "confidence": 0.88,
                        "event_date": date(2026, 2, 11),
                    },
                    {
                        "category": "diagnosis",
                        "title": "Hipertension arterial",
                        "description": "Presion arterial elevada en consulta.",
                        "source_quote": "TA 150/95.",
                        "confidence": 0.92,
                        "event_date": date(2026, 2, 11),
                    },
                ],
            },
            {
                "date": date(2026, 3, 2),
                "type": "Revision",
                "note_text": "Analitica con colesterol LDL elevado. Se inicia atorvastatina 20 mg.",
                "events": [
                    {
                        "category": "lab",
                        "title": "LDL elevado",
                        "description": "Resultado de laboratorio con LDL por encima de rango.",
                        "source_quote": "Analitica con colesterol LDL elevado.",
                        "confidence": 0.9,
                        "event_date": date(2026, 3, 2),
                    },
                    {
                        "category": "medication",
                        "title": "Inicio de atorvastatina",
                        "description": "Se pauta atorvastatina 20 mg diaria.",
                        "source_quote": "Se inicia atorvastatina 20 mg.",
                        "confidence": 0.94,
                        "event_date": date(2026, 3, 2),
                    },
                ],
            },
        ],
    },
    {
        "patient": {
            "name": "Daniel Ortega",
            "birth_date": date(1973, 9, 5),
            "sex": "M",
        },
        "encounters": [
            {
                "date": date(2026, 1, 20),
                "type": "Urgencias",
                "note_text": "Dolor toracico opresivo de 30 minutos. ECG sin elevacion de ST.",
                "events": [
                    {
                        "category": "symptom",
                        "title": "Dolor toracico",
                        "description": "Episodio de dolor toracico opresivo.",
                        "source_quote": "Dolor toracico opresivo de 30 minutos.",
                        "confidence": 0.9,
                        "event_date": date(2026, 1, 20),
                    },
                    {
                        "category": "procedure",
                        "title": "Electrocardiograma",
                        "description": "ECG realizado en urgencias.",
                        "source_quote": "ECG sin elevacion de ST.",
                        "confidence": 0.87,
                        "event_date": date(2026, 1, 20),
                    },
                ],
            },
            {
                "date": date(2026, 1, 28),
                "type": "Cardiologia",
                "note_text": "Se realiza ergometria negativa para isquemia. Seguimiento en 6 meses.",
                "events": [
                    {
                        "category": "procedure",
                        "title": "Ergometria",
                        "description": "Prueba de esfuerzo sin hallazgos de isquemia.",
                        "source_quote": "Ergometria negativa para isquemia.",
                        "confidence": 0.91,
                        "event_date": date(2026, 1, 28),
                    }
                ],
            },
        ],
    },
    {
        "patient": {
            "name": "Rocio Mendez",
            "birth_date": date(1994, 12, 1),
            "sex": "F",
        },
        "encounters": [
            {
                "date": date(2026, 4, 7),
                "type": "Atencion primaria",
                "note_text": "Tos seca y fiebre de 38.2C. Se pauta ibuprofeno y reposo.",
                "events": [
                    {
                        "category": "symptom",
                        "title": "Fiebre",
                        "description": "Temperatura corporal elevada.",
                        "source_quote": "fiebre de 38.2C",
                        "confidence": 0.89,
                        "event_date": date(2026, 4, 7),
                    },
                    {
                        "category": "medication",
                        "title": "Ibuprofeno",
                        "description": "Tratamiento sintomatico con ibuprofeno.",
                        "source_quote": "Se pauta ibuprofeno y reposo.",
                        "confidence": 0.93,
                        "event_date": date(2026, 4, 7),
                    },
                ],
            }
        ],
    },
]


def get_or_create_patient(db, payload: dict) -> Patient:
    stmt = select(Patient).where(
        Patient.name == payload["name"],
        Patient.birth_date == payload["birth_date"],
        Patient.sex == payload["sex"],
    )
    patient = db.execute(stmt).scalars().first()
    if patient:
        return patient

    patient = Patient(**payload)
    db.add(patient)
    db.flush()
    return patient


def get_or_create_encounter(db, patient_id: str, payload: dict) -> Encounter:
    stmt = select(Encounter).where(
        Encounter.patient_id == patient_id,
        Encounter.date == payload["date"],
        Encounter.type == payload["type"],
        Encounter.note_text == payload["note_text"],
    )
    encounter = db.execute(stmt).scalars().first()
    if encounter:
        return encounter

    encounter = Encounter(
        patient_id=patient_id,
        date=payload["date"],
        type=payload["type"],
        note_text=payload["note_text"],
    )
    db.add(encounter)
    db.flush()
    return encounter


def ensure_events(db, patient_id: str, encounter: Encounter, events_payload: list[dict]) -> int:
    existing = db.execute(
        select(ClinicalEvent).where(ClinicalEvent.encounter_id == encounter.id)
    ).scalars().all()
    if existing:
        return 0

    for event in events_payload:
        db.add(
            ClinicalEvent(
                encounter_id=encounter.id,
                patient_id=patient_id,
                category=event["category"],
                title=event["title"],
                description=event["description"],
                source_quote=event["source_quote"],
                confidence=event["confidence"],
                event_date=event["event_date"],
            )
        )
    return len(events_payload)


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    created_patients = 0
    created_encounters = 0
    created_events = 0

    try:
        for entry in SEED_DATA:
            patient_payload = entry["patient"]
            patient_before = db.execute(
                select(Patient).where(
                    Patient.name == patient_payload["name"],
                    Patient.birth_date == patient_payload["birth_date"],
                    Patient.sex == patient_payload["sex"],
                )
            ).scalars().first()
            patient = get_or_create_patient(db, patient_payload)
            if not patient_before:
                created_patients += 1

            for enc_payload in entry["encounters"]:
                encounter_before = db.execute(
                    select(Encounter).where(
                        Encounter.patient_id == patient.id,
                        Encounter.date == enc_payload["date"],
                        Encounter.type == enc_payload["type"],
                        Encounter.note_text == enc_payload["note_text"],
                    )
                ).scalars().first()
                encounter = get_or_create_encounter(db, patient.id, enc_payload)
                if not encounter_before:
                    created_encounters += 1

                created_events += ensure_events(
                    db,
                    patient.id,
                    encounter,
                    enc_payload["events"],
                )

        db.commit()
        print(
            f"Seed completado. Nuevos pacientes={created_patients}, "
            f"encuentros={created_encounters}, eventos={created_events}."
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
