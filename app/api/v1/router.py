from fastapi import APIRouter
from .endpoints.health import router as health_router
from .endpoints.item import router as items_router
from .endpoints.root import router as root

api_def_router = APIRouter()
api_def_router.include_router(root)

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(items_router)

