from fastapi import APIRouter
from .health import router as health_router
from .root import router as root

router = APIRouter()
router.include_router(health_router)
router.include_router(root)