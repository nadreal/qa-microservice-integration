import pytest
import logging

@pytest.mark.integration
def test_create_item_persisted_in_db(client, db_connection, unique_item_payload):
    # Create unique item payload
    payload = unique_item_payload()

    #Step 1: Create item via API
    response = client.post("/api/v1/items/", json=payload)
    
    # Step 2: Validate API response
    assert response.status_code == 201, response.text
    created_item = response.json()

    item_id = created_item["id"]

    # Step 3: Query DB directly
    cursor = db_connection.cursor()
    cursor.execute(
        """
        SELECT id, name, description, created_at 
        FROM items WHERE id = %s""",
        (item_id,)
    )

    db_item = cursor.fetchone()

    print(f"Created item ID: {item_id}")
    print(f"DB row: id={db_item[0]}, name={db_item[1]}")
    
    
    # Step 4: Validate DB record
    assert db_item is not None
    assert db_item[0] == item_id
    assert db_item[1] == payload["name"]
    assert db_item[2] == payload["description"]
    
    
@pytest.mark.integration
def test_update_item_persists_in_db(client, db_connection, created_item):
    new_name = "Updated_Name"

    response = client.put(
        f"/api/v1/items/{created_item['id']}",
        json={"name": new_name, "description": created_item["description"]}
    )

    assert response.status_code == 200

    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT name FROM items WHERE id = %s",
        (created_item["id"],)
    )

    db_item = cursor.fetchone()

    assert db_item[0] == new_name
    
@pytest.mark.integration
def test_delete_item_removes_from_db(client, db_connection, created_item):
    item_id = created_item["id"]

    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code in [200, 204]

    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM items WHERE id = %s",
        (item_id,)
    )

    db_item = cursor.fetchone()

    assert db_item is None
    
    
@pytest.mark.integration
def test_duplicate_item_name_fails(client, unique_item_payload):
    payload = unique_item_payload()

    r1 = client.post("/api/v1/items/", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/v1/items/", json=payload)
    assert r2.status_code in [400, 409]
    
@pytest.mark.integration
def test_item_without_description_is_saved(client, db_connection, unique_item_payload):
    payload = unique_item_payload()
    payload.pop("description")

    response = client.post("/api/v1/items/", json=payload)
    assert response.status_code == 201

    item_id = response.json()["id"]

    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT description FROM items WHERE id = %s",
        (item_id,)
    )

    db_item = cursor.fetchone()

    assert db_item[0] is None
    
@pytest.mark.integration
def test_created_at_is_set(client, db_connection, unique_item_payload):
    payload = unique_item_payload()

    response = client.post("/api/v1/items/", json=payload)
    item_id = response.json()["id"]

    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT created_at FROM items WHERE id = %s",
        (item_id,)
    )

    db_item = cursor.fetchone()

    assert db_item[0] is not None