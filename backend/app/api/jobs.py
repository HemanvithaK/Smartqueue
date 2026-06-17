import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.deps import get_current_user
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreateRequest, JobResponse
from app.workers.tasks import process_dummy_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = Job(
        tenant_id=current_user.tenant_id,
        created_by=current_user.id,
        job_type=payload.job_type,
        status="queued",
        payload=payload.payload,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Send to Celery — for now everything routes to the dummy task
    process_dummy_job.delay(str(job.id), payload.payload)

    return job


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # CRITICAL: filtered by tenant_id — this IS the isolation boundary
    result = await db.execute(
        select(Job).where(Job.tenant_id == current_user.tenant_id).order_by(Job.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.tenant_id == current_user.tenant_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        # 404, not 403 — don't reveal whether the job exists for another tenant
        raise HTTPException(status_code=404, detail="Job not found")
    return job