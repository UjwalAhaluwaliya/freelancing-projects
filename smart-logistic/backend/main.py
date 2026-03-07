from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, shipments, vehicles, tracking, ai, analytics, notifications, users, chatbot

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Smart Logistics Management System",
    description="Intelligent logistics management with AI-powered route optimization, demand forecasting, and ETA prediction.",
    version="1.0.0",
)

# CORS - allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    # wildcard sometimes doesn’t work reliably for preflighted auth headers;
    # explicitly permit Authorization and content-type
    allow_headers=["Authorization", "Content-Type"],
)

# Register routers
app.include_router(auth.router)
app.include_router(shipments.router)
app.include_router(vehicles.router)
app.include_router(tracking.router)
app.include_router(ai.router)
app.include_router(analytics.router)
app.include_router(notifications.router)
app.include_router(users.router)
app.include_router(chatbot.router)


@app.get("/")
def root():
    return {"message": "AI Smart Logistics Management System API", "docs": "/docs"}
