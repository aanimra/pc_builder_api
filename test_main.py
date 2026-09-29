from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id_success():
    response = client.get("/api/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "AMD Ryzen 5 5600X"

def test_get_item_by_id_not_found():
    response = client.get("/api/items/9999")
    assert response.status_code == 404

def test_create_item():
    payload = {
        "name": "Kingston Fury Beast 16GB",
        "category": "RAM",
        "price": 42.50,
        "stock": 20,
        "description": "DDR4 3200MHz"
    }
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]

def test_update_item():
    payload = {
        "name": "AMD Ryzen 5 5600X (Updated)",
        "category": "CPU",
        "price": 139.99,
        "stock": 10,
        "description": "Ціну знижено"
    }
    response = client.put("/api/items/1", json=payload)
    assert response.status_code == 200
    assert response.json()["price"] == 139.99

def test_delete_item():
    response = client.delete("/api/items/2")
    assert response.status_code == 204
    get_res = client.get("/api/items/2")
    assert get_res.status_code == 404
    