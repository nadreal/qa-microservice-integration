import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.schemas.item import ItemRead

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_items_endpoint():
    mock_items = [ItemRead(id=1, name="TestItem", description="Desc")]

    with patch("app.api.v1.endpoints.item.ItemService.list_items", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = mock_items
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "TestItem"


@pytest.mark.asyncio
async def test_get_item_by_id_endpoint_found():
    mock_item = ItemRead(id=1, name="FoundItem", description="Desc")

    with patch("app.api.v1.endpoints.item.ItemService.get_item_by_id", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_item
        response = client.get("/api/v1/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "FoundItem"


@pytest.mark.asyncio
async def test_get_item_by_id_endpoint_not_found():
    with patch("app.api.v1.endpoints.item.ItemService.get_item_by_id", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None
        response = client.get("/api/v1/items/999")
        assert response.status_code == 404