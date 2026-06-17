from fastapi import FastAPI
from app.api import auth, jobs

app = FastAPI(title="SmartQueue API", version="0.1.0")

app.include_router(auth.router)
app.include_router(jobs.router)


@app.get("/health")
async def health():
    return {"status": "ok"}