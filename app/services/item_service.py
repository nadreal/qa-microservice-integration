
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update

from app.models.item import Item

class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_items(self):
        result = await self.session.execute(select(Item))
        return result.scalars().all()

    async def get_item_by_id(self, item_id: int):
        result = await self.session.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    async def create_item(self, name: str, description: str = None):
        item = Item(name=name, description=description)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
    
    async def update_item(self, item_id: int, name: str = None, description: str = None):
        item = await self.get_item_by_id(item_id)
        
        if not item:
            return None
        if name:
            item.name = name
        if description:
            item.description = description
        
        await self.session.commit()
        await self.session.refresh(item)
        return item
    
    async def delete_item(self, item_id: int):
        item = await self.get_item_by_id(item_id)
        if not item:
            return None
        await self.session.delete(item)
        await self.session.commit()
        return item 
    
    
