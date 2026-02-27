import pytest

@pytest.mark.integration
def test_list_items_includes_created_item(client, created_item):
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert any(i["id"] == created_item["id"] for i in items)

@pytest.mark.integration
def test_update_item_updates_name_and_description(client, created_item, unique_item_payload):
    new_payload = unique_item_payload(description="UpdatedDesc")
    response = client.put(
        f"/api/v1/items/{created_item['id']}",
        json={"name": new_payload["name"], "description": new_payload["description"]},
    )
    assert response.status_code == 200, response.text
    updated = response.json()
    assert updated["id"] == created_item["id"]
    assert updated["name"] == new_payload["name"]
    assert updated["description"] == new_payload["description"]

    # Verify persisted
    r2 = client.get(f"/api/v1/items/{created_item['id']}")
    assert r2.status_code == 200
    persisted = r2.json()
    assert persisted["name"] == new_payload["name"]
    assert persisted["description"] == new_payload["description"]

@pytest.mark.integration
def test_update_item_partial_does_not_wipe_description(client, created_item, unique_item_payload):
    # Change ONLY name
    new_name = unique_item_payload()["name"]

    response = client.put(f"/api/v1/items/{created_item['id']}", json={"name": new_name})
    assert response.status_code == 200, response.text
    updated = response.json()

    assert updated["name"] == new_name
    # This is the key check (PUT behaves like PATCH in your implementation)
    assert updated["description"] == created_item["description"]

@pytest.mark.integration
def test_update_item_invalid_payload_returns_422(client, created_item):
    response = client.put(f"/api/v1/items/{created_item['id']}", json={"name": 123})
    assert response.status_code == 422

@pytest.mark.integration
def test_list_items_returns_200_and_list_shape(client):
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)