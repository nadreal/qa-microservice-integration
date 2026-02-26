from fastapi import FastAPI
from app.api.v1.router import api_v1_router, api_def_router

app = FastAPI(title="QA Microservice Integration")
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(api_def_router)
