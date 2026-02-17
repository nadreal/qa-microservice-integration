from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.item import Item

class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Item))
        return result.scalars().all()

    async def get_by_id(self, item_id: int):
        result = await self.session.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    async def create(self, name: str, description: str = None):
        item = Item(name=name, description=description)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
