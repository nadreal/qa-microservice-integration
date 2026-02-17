from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def list_items(db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.list_items()

@router.post("/")
async def create_item(name: str, description: str = None, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.create_item(name, description)

