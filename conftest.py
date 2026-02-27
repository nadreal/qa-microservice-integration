import os
import pytest
import httpx
import uuid

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as c:
        yield c 

@pytest.fixture
def unique_item_payload():
    def make(description: str = "TestDescription", name_prefix: str = "TestItem"):
        return {
            "name": f"TestItem_{uuid.uuid4().hex}",
            "description": "TestDescription",
        }
    return make

@pytest.fixture
def created_item(client, unique_item_payload):
    r = client.post("/api/v1/items/", json=unique_item_payload())
    assert r.status_code == 201, r.text
    item = r.json()
    yield item

    try:
        client.delete(f"/api/v1/items/{item['id']}")
    except Exception:
        pass