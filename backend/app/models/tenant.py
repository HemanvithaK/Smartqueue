import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # Plan controls rate limits / priority later
    plan: Mapped[str] = mapped_column(String(50), default="free")  # free | pro | enterprise

    # Monthly AI budget cap in USD cents — enforced in Phase 2
    monthly_budget_cents: Mapped[int] = mapped_column(default=500)  # $5 free tier default

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())