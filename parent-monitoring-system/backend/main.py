from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import close_mongodb_connection, connect_to_mongodb
from .routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan: connect on startup, disconnect on shutdown."""
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="AI Parental Control System API",
    description="Backend API for mobile-based AI Parental Control System",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy"}
