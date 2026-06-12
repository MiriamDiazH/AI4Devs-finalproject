from app.services.statewave_service import StatewaveService


class ExtractionService:
    def __init__(self):
        self.statewave_service = StatewaveService()

    def extract_from_note(
        self,
        patient_id: str,
        encounter_id: str,
        note_text: str,
    ) -> list[dict]:
        return self.statewave_service.extract_events(
            patient_id=patient_id,
            encounter_id=encounter_id,
            note_text=note_text,
        )
