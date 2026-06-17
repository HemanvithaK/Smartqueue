import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # The isolation boundary — same pattern as User
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    # What kind of job this is — "summarize" | "classify" | "extract" | "dummy"
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # queued -> processing -> completed | failed
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)

    # The input data sent by the user (flexible JSON, since different job types need different inputs)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    # The output once the job completes
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # If it failed, why
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # How many times we've retried this job
    retry_count: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())