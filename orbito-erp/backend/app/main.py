from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase
from app.core.config import settings
from app.routers import (
    notifications,
    profile,
    leave,
    job,
    candidate,
    application,
    interview,
    achievement,
    dashboard,
    auth,
    ai,
)

app = FastAPI(title="Orbito ERP Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router)
app.include_router(leave.router)
app.include_router(notifications.router)
app.include_router(job.router)
app.include_router(candidate.router)
app.include_router(application.router)
app.include_router(interview.router)
app.include_router(achievement.router)
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(ai.router)


@app.get("/")
def home():
    return {"message": "Orbito Backend Running"}


@app.get("/test-db")
def test_database():
    response = supabase.table("profiles").select("*").execute()
    return {"status": "connected", "data": response.data}
