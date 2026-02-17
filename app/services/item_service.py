from app.repositories.item_repository import ItemRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ItemService:
    def __init__(self, session: AsyncSession):
        self.repo = ItemRepository(session)

    async def list_items(self):
        return await self.repo.get_all()

    async def get_item(self, item_id: int):
        return await self.repo.get_by_id(item_id)

    async def create_item(self, name: str, description: str = None):
        # Here you could add business rules, validation, etc.
        return await self.repo.create(name, description)
