from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import String, Date, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    patient_id: Mapped[str] = mapped_column(
        String, ForeignKey("patients.id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    note_text: Mapped[str] = mapped_column(Text, nullable=False)

    patient: Mapped["Patient"] = relationship(back_populates="encounters")
    clinical_events: Mapped[list["ClinicalEvent"]] = relationship(
        back_populates="encounter", cascade="all, delete-orphan"
    )
