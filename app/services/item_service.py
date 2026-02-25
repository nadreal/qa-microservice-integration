from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update

from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
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

    async def create_item(self, item:ItemCreate):
        db_item = Item(name=item.name, description=item.description)
        self.session.add(db_item)
        try:
            await self.session.commit()
            await self.session.refresh(db_item)
            return db_item
        except IntegrityError:
            await self.session.rollback()
            raise
        
    
    async def update_item(self, item_id: int, update_item: ItemUpdate):
        db_item = await self.get_item_by_id(item_id)
        if not db_item:
            return None
        
        if update_item.name is not None:
            db_item.name = update_item.name
        if update_item.description is not None:
            db_item.description = update_item.description
        
        try:
            await self.session.commit()
            await self.session.refresh(db_item)
            return db_item    
        except IntegrityError:
            await self.session.rollback()
            raise
        
    async def delete_item(self, item_id: int):
        item = await self.get_item_by_id(item_id)
        if not item:
            return None
        try:
            await self.session.delete(item)
            await self.session.commit()
            return item
        except IntegrityError: 
            await self.session.rollback()
            raise
       
    
    
