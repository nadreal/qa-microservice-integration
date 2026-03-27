import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError

from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemUpdate
from app.models.item import Item


@pytest.fixture
def mock_session():
    """Mock async SQLAlchemy session."""
    session = MagicMock()  # sync base
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session    


@pytest.fixture
def service(mock_session):
    """ItemService instance with mocked session."""
    return ItemService(session=mock_session)


@pytest.mark.asyncio
async def test_list_items(service, mock_session):
    """Test listing items returns a list of items."""
    mock_item = Item(id=1, name="TestItem", description="A test item")

    # Scalars().all() chain must return a list
    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value.all.return_value = [mock_item]

    # session.execute is async
    mock_session.execute = AsyncMock(return_value=mock_execute_result)

    items = await service.list_items()
    assert len(items) == 1
    assert items[0].name == "TestItem"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_item_success(service, mock_session):
    """Test creating an item succeeds and commits."""
    item_create = ItemCreate(name="NewItem", description="New item desc")

    # session.commit() and session.refresh() are async
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    created_item = await service.create_item(item_create)

    assert created_item.name == "NewItem"
    assert created_item.description == "New item desc"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    

@pytest.mark.asyncio
async def test_get_item_by_id_found(service, mock_session):
    """Test getting an item by ID returns the item if found."""
    mock_item = Item(id=1, name="FoundItem", description="Desc")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_item
    mock_session.execute = AsyncMock(return_value=mock_result)

    item = await service.get_item_by_id(1)
    assert item.name == "FoundItem"


@pytest.mark.asyncio
async def test_get_item_by_id_not_found(service, mock_session):
    """Test getting an item by ID returns None if not found."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    item = await service.get_item_by_id(999)
    assert item is None


@pytest.mark.asyncio
async def test_create_item_integrity_error(service, mock_session):
    """Test create_item raises IntegrityError and rolls back."""
    item_create = ItemCreate(name="DupItem", description="Desc")
    
    mock_session.commit = AsyncMock(side_effect=IntegrityError(statement=None, params=None, orig=None))
    mock_session.rollback = AsyncMock()

    with pytest.raises(IntegrityError):
        await service.create_item(item_create)
    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_update_item_success(service, mock_session):
    """Test updating an item updates fields and commits."""
    existing_item = Item(id=1, name="Old", description="OldDesc")
    service.get_item_by_id = AsyncMock(return_value=existing_item)
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    update_data = ItemUpdate(name="New", description="NewDesc")
    updated_item = await service.update_item(1, update_data)
    assert updated_item.name == "New"
    assert updated_item.description == "NewDesc"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_item_not_found(service):
    """Test updating a non-existent item returns None."""
    service.get_item_by_id = AsyncMock(return_value=None)
    update_data = ItemUpdate(name="New")
    updated_item = await service.update_item(999, update_data)
    assert updated_item is None


@pytest.mark.asyncio
async def test_delete_item_success(service, mock_session):
    """Test deleting an item succeeds and commits."""
    item = Item(id=1, name="ToDelete", description="Desc")
    service.get_item_by_id = AsyncMock(return_value=item)
    mock_session.commit.return_value = None
    mock_session.delete.return_value = None

    deleted = await service.delete_item(1)
    assert deleted == item
    mock_session.commit.assert_called_once()
    mock_session.delete.assert_called_once_with(item)


@pytest.mark.asyncio
async def test_delete_item_not_found(service):
    """Test deleting a non-existent item returns None."""
    service.get_item_by_id = AsyncMock(return_value=None)
    deleted = await service.delete_item(999)
    assert deleted is None