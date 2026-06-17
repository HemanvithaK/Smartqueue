import time
import uuid
from app.workers.celery_app import celery_app
from app.database import SyncSessionLocal
from app.models.tenant import Tenant  # noqa: F401 — registers table in SA metadata
from app.models.user import User      # noqa: F401 — registers table in SA metadata
from app.models.job import Job


@celery_app.task(name="process_dummy_job", bind=True, max_retries=3)
def process_dummy_job(self, job_id: str, payload: dict):
    db = SyncSessionLocal()
    try:
        job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()
        if not job:
            print(f"[Worker] Job {job_id} not found in DB — skipping")
            return

        # Mark as processing the moment we pick it up
        job.status = "processing"
        db.commit()
        print(f"[Worker] Starting job {job_id} with payload: {payload}")

        time.sleep(5)  # simulate work being done

        result = {
            "message": "Dummy job completed successfully",
            "input_received": payload,
        }

        # Mark as completed with the actual result
        job.status = "completed"
        job.result = result
        db.commit()
        print(f"[Worker] Finished job {job_id}")

        return result

    except Exception as exc:
        job.status = "failed"
        job.error_message = str(exc)
        db.commit()
        print(f"[Worker] Job {job_id} failed: {exc}")
        raise

    finally:
        db.close()