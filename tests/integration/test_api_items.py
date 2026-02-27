import pytest
import httpx

@pytest.mark.integration
def test_create_item_returns_id(created_item):
    assert "id" in created_item
    assert created_item["name"].startswith("TestItem_")


@pytest.mark.integration
def test_get_item_by_id(client, created_item):
    item_id = created_item["id"]
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"]== created_item["name"]
    

@pytest.mark.integration
def test_delete_item(client, created_item):
    item_id = created_item["id"]
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code in (200, 204)
   
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404
       
@pytest.mark.integration        
def test_get_missing_item_returns_404(client):     
    response = client.get(f"/api/v1/items/4444444")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
    
    
@pytest.mark.integration
def test_delete_missing_item_returns_404(client):
    r = client.delete("/api/v1/items/4444444")
    assert r.status_code == 404
    assert r.json()["detail"] == "Item not found"


@pytest.mark.integration
def test_update_missing_item_returns_404(client):
    r = client.put("/api/v1/items/4444444", json={"name": "does_not_matter"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Item not found"


@pytest.mark.integration
def test_create_missing_required_field_name_returns_422(client):
    r = client.post("/api/v1/items/", json={"description": "x"})
    assert r.status_code == 422  # Pydantic validation


@pytest.mark.integration
def test_create_name_wrong_type_returns_422(client):
    r = client.post("/api/v1/items/", json={"name": 123, "description": "x"})
    assert r.status_code == 422


@pytest.mark.integration
def test_create_duplicate_name_returns_409(client, unique_item_payload):    
    payload = unique_item_payload()
    r1 = client.post("/api/v1/items/", json=payload)
    assert r1.status_code == 201, r1.text
    item = r1.json()

    try:
        r2 = client.post("/api/v1/items/", json=payload)
        assert r2.status_code == 409, r2.text
        assert "already exists" in r2.json()["detail"]
    finally:
        client.delete(f"/api/v1/items/{item['id']}")


@pytest.mark.integration
def test_update_duplicate_name_returns_409(client, unique_item_payload):    
    p1 = unique_item_payload()
    p2 = unique_item_payload()
    
    r1 = client.post("/api/v1/items/", json=p1)
    r2 = client.post("/api/v1/items/", json=p2)
    
    assert r1.status_code == 201, r1.text 
    assert r2.status_code == 201, r2.text

    item1 = r1.json()
    item2 = r2.json()

    try:
        # Try rename item2 to item1's name -> should conflict
        r = client.put(f"/api/v1/items/{item2['id']}", json={"name": item1["name"]})
        assert r.status_code == 409, r.text
    finally:
        client.delete(f"/api/v1/items/{item1['id']}")
        client.delete(f"/api/v1/items/{item2['id']}")