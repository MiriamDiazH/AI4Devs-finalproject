from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ClinicalEvent(Base):
    __tablename__ = "clinical_events"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    encounter_id: Mapped[str] = mapped_column(
        String, ForeignKey("encounters.id"), nullable=False
    )
    patient_id: Mapped[str] = mapped_column(
        String, ForeignKey("patients.id"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_quote: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    event_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    encounter: Mapped["Encounter"] = relationship(back_populates="clinical_events")
