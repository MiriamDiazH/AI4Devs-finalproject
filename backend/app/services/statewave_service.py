import httpx
import json
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "event_extraction.txt"


class StatewaveService:
    """Statewave integration for contextual extraction and memory hooks."""

    def __init__(self):
        self.base_url = settings.statewave_url.rstrip("/")
        self.timeout = settings.statewave_timeout_seconds
        self.episode_path = settings.statewave_episode_path
        self.compile_path = settings.statewave_compile_path
        self.context_path = settings.statewave_context_path
        self.llm_complete_path = settings.statewave_llm_complete_path
        self.subject_prefix = settings.statewave_subject_prefix
        self.context_max_tokens = settings.statewave_context_max_tokens
        self.extraction_temperature = settings.statewave_extraction_temperature
        self.extraction_max_tokens = settings.statewave_extraction_max_tokens
        self._system_prompt = _PROMPT_PATH.read_text()

    def extract_events(
        self,
        patient_id: str,
        encounter_id: str,
        note_text: str,
    ) -> list[dict]:
        subject_id = f"{self.subject_prefix}:{patient_id}"

        context_text = note_text
        try:
            with httpx.Client(timeout=self.timeout) as client:
                # 1) Ingest encounter note as a Statewave episode.
                ingest_payload = {
                    "subject_id": subject_id,
                    "source": "auditcare-backend",
                    "type": "clinical.note",
                    "payload": {
                        "encounter_id": encounter_id,
                        "text": note_text,
                    },
                    "occurred_at": datetime.now(timezone.utc).isoformat(),
                }
                ingest_response = client.post(
                    f"{self.base_url}{self.episode_path}",
                    json=ingest_payload,
                )
                ingest_response.raise_for_status()

                # 2) Compile memories for the patient subject.
                compile_response = client.post(
                    f"{self.base_url}{self.compile_path}",
                    json={"subject_id": subject_id},
                )
                compile_response.raise_for_status()

                # 3) Retrieve assembled context to drive extraction.
                context_response = client.post(
                    f"{self.base_url}{self.context_path}",
                    json={
                        "subject_id": subject_id,
                        "task": "Extract structured clinical events",
                        "max_tokens": self.context_max_tokens,
                    },
                )
                context_response.raise_for_status()
                context_json = context_response.json()
                assembled_context = context_json.get("assembled_context", "")
                if assembled_context and assembled_context.strip():
                    # Keep the original clinical note to avoid empty extraction when
                    # assembled context is sparse (for example, only task headers).
                    context_text = f"{note_text}\n\n{assembled_context}"
                else:
                    context_text = note_text
        except httpx.HTTPError:
            # Fallback keeps the flow alive if Statewave is temporarily unavailable.
            context_text = note_text

        return self._extract_events_with_statewave_llm(context_text)

    def _extract_events_with_statewave_llm(self, context_text: str) -> list[dict]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                llm_response = client.post(
                    f"{self.base_url}{self.llm_complete_path}",
                    json={
                        "messages": [
                            {"role": "system", "content": self._system_prompt},
                            {"role": "user", "content": context_text},
                        ],
                        "temperature": self.extraction_temperature,
                        "max_tokens": self.extraction_max_tokens,
                    },
                )
                llm_response.raise_for_status()
                reply = llm_response.json().get("reply", "{}")
        except httpx.HTTPError:
            return []

        try:
            normalized_reply = reply.strip()
            if normalized_reply.startswith("```"):
                normalized_reply = normalized_reply.strip("`")
                if normalized_reply.lower().startswith("json"):
                    normalized_reply = normalized_reply[4:].strip()

            data = json.loads(normalized_reply)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                events = data.get("events", [])
                return events if isinstance(events, list) else []
            return []
        except json.JSONDecodeError:
            return []

    def get_patient_status(self, patient_id: str) -> dict:
        """Get Statewave status for a patient."""
        subject_id = f"{self.subject_prefix}:{patient_id}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                # Try to fetch context to verify subject exists and has data
                context_response = client.post(
                    f"{self.base_url}{self.context_path}",
                    json={
                        "subject_id": subject_id,
                        "task": "Status check",
                        "max_tokens": 500,
                    },
                )
                context_response.raise_for_status()
                context_json = context_response.json()
                assembled = context_json.get("assembled_context", "")
                
                if assembled and len(assembled.strip()) > 0:
                    return {
                        "subject_id": subject_id,
                        "is_available": True,
                        "status": "healthy",
                        "message": f"Statewave active with compiled memories for {patient_id}",
                        "context_preview": assembled[:200] + "..." if len(assembled) > 200 else assembled,
                    }
                else:
                    return {
                        "subject_id": subject_id,
                        "is_available": True,
                        "status": "no_data",
                        "message": f"Statewave available but no memories yet for {patient_id}",
                        "context_preview": None,
                    }
        except httpx.HTTPError as e:
            return {
                "subject_id": subject_id,
                "is_available": False,
                "status": "error",
                "message": f"Statewave unavailable: {str(e)}",
                "context_preview": None,
            }

    def save_patient_context(self, patient_id: str, payload: dict) -> dict:
        return {"patient_id": patient_id, "saved": True}
