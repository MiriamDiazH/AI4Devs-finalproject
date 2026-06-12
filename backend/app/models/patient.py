from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(10), nullable=False)

    encounters: Mapped[list["Encounter"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
