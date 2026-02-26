from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

@router.get("/" ,include_in_schema=False)
def api_root():
    return {
        "service": "qa-microservice-integration",
        "version": "v1",        
        "docs": "/docs",
        "api": "/api/v1",
        "health": "/api/v1/health"
    }

@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)