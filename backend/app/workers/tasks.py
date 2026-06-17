import time
from app.workers.celery_app import celery_app


@celery_app.task(name="process_dummy_job", bind=True, max_retries=3)
def process_dummy_job(self, job_id: str, payload: dict):
    """
    A fake job that just waits 5 seconds and returns a canned response.
    This proves the queue infrastructure works before we add real AI logic.
    """
    print(f"[Worker] Starting job {job_id} with payload: {payload}")
    time.sleep(5)  # simulate work being done
    result = {
        "message": "Dummy job completed successfully",
        "input_received": payload,
    }
    print(f"[Worker] Finished job {job_id}")
    return result