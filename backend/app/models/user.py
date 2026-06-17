import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # Every user belongs to exactly one tenant — this IS the isolation boundary
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # admin | member — admin can manage API keys, member cannot
    role: Mapped[str] = mapped_column(String(20), default="member")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())