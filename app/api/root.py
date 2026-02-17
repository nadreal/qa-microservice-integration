from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message" : "QA Microservice Integration is running"}