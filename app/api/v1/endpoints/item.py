from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def list_items(db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.list_items()

@router.get("/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/")
async def create_item(name: str, description: str = None, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.create_item(name, description)

@router.put("/{item_id}")
async def update_item(item_id: int, name:str, description: str = None, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    updated = await service.update_item(item_id, name, description)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.delete_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item