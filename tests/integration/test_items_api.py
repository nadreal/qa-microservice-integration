import pytest
import httpx

@pytest.mark.positive
async def test_create_item_returns_id(created_item):
    assert "id" in created_item
    assert created_item["name"].startswith("TestItem_")

@pytest.mark.positive
async def test_get_item_by_id(client, created_item):
    item_id = created_item["id"]
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"]== created_item["name"]
    
@pytest.mark.positive
async def test_delete_item(client, created_item):
    item_id = created_item["id"]
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code in (200, 204)
   
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404

@pytest.mark.negative
def test_create_duplicate_name_returns_409(client, unique_item_payload):
    r1 = client.post("/api/v1/items/", json=unique_item_payload)
    assert r1.status_code == 200, r1.text
    item = r1.json()

    try:
        r2 = client.post("/api/v1/items/", json=unique_item_payload)
        assert r2.status_code == 409, r2.text
    finally:
        try:
            client.delete(f"/api/v1/items/{item['id']}")
        except httpx.HTTPError:
            pass