import pytest
from fastapi.testclient import TestClient

from main import app, items_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    items_db.clear()
    yield
    items_db.clear()


def test_list_items_empty():
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_and_get_item():
    resp = client.post("/items", json={"name": "Pen", "price": 1.5})
    assert resp.status_code == 201
    created = resp.json()
    assert created["name"] == "Pen"
    assert created["description"] is None
    assert isinstance(created["id"], int)

    resp = client.get(f"/items/{created['id']}")
    assert resp.status_code == 200
    assert resp.json() == created

    resp = client.get("/items")
    assert resp.json() == [created]


def test_get_item_not_found():
    resp = client.get("/items/9999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Item not found"}


def test_create_item_validation_error():
    resp = client.post("/items", json={"name": "", "price": -1})
    assert resp.status_code == 422
