
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete, update
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead

from app.db.models.item import Item

class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_items(self):
        result = await self.session.execute(select(Item))
        return result.scalars().all()

    async def get_item_by_id(self, item_id: int):
        result = await self.session.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    async def create_item(self, item:ItemCreate):
        db_item = Item(name=item.name, description=item.description)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item
    
    async def update_item(self, item_id: int, update_item:ItemCreate):
        db_item = await self.get_item_by_id(item_id)
        
        if not db_item:
            return None
        if update_item.name:
            db_item.name = update_item.name
        if update_item.description:
            db_item.description = update_item.description
        
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item
    
    async def delete_item(self, item_id: int):
        item = await self.get_item_by_id(item_id)
        if not item:
            return None
        await self.session.delete(item)
        await self.session.commit()
        return item 
    
    
