from pydantic import BaseModel


class StatewaveStatusResponse(BaseModel):
    """Status of Statewave integration for a patient."""

    subject_id: str
    is_available: bool
    status: str  # "healthy", "no_data", "error"
    message: str
    context_preview: str | None = None

    class Config:
        from_attributes = True
