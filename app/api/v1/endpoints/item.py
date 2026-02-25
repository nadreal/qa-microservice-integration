from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db.session import get_db
from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[ItemRead])
async def list_items(db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.list_items()

@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemRead)
async def create_item(
    item: ItemCreate, 
    db: AsyncSession = Depends(get_db)
    ):
    service = ItemService(db)
    try:
        return await service.create_item(item)  
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="item with this name already exists")
        raise HTTPException(status_code=418, detail="create_item reached")

@router.put("/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item_update:ItemUpdate, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)    
    updated = await service.update_item(item_id, item_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", response_model=ItemRead)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.delete_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item