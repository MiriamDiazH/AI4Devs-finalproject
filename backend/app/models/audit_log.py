from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
