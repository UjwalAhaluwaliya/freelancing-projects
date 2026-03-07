from fastapi import APIRouter

from .alerts import router as alerts_router
from .auth import router as auth_router
from .child import router as child_router
from .reports import router as reports_router
from .safety import router as safety_router
from .screen_time import router as screen_time_router

api_router = APIRouter(tags=["api"])
api_router.include_router(auth_router)
api_router.include_router(child_router)
api_router.include_router(screen_time_router)
api_router.include_router(alerts_router)
api_router.include_router(reports_router)
api_router.include_router(safety_router)
