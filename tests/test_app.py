import pytest
from app import create_app
from app.models import db, CarOwner, Car


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/api/login", json={"username": "admin", "password": "password"}
    )
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_add_car_owner(client, auth_headers):
    response = client.post(
        "/api/car_owners", json={"name": "John Doe"}, headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json["name"] == "John Doe"


def test_add_car(client, auth_headers):
    # Adicionando um proprietário
    client.post("/api/car_owners", json={"name": "Jane Doe"}, headers=auth_headers)

    # Adicionando um carro para este proprietário
    response = client.post(
        "/api/cars",
        json={"color": "blue", "model": "sedan", "owner_id": 1},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json["color"] == "blue"
    assert response.json["model"] == "sedan"
    assert response.json["owner_id"] == 1


def test_get_car_owners(client, auth_headers):
    client.post("/api/car_owners", json={"name": "Alice"}, headers=auth_headers)
    client.post("/api/car_owners", json={"name": "Bob"}, headers=auth_headers)

    response = client.get("/api/car_owners", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_cars(client, auth_headers):
    client.post("/api/car_owners", json={"name": "Charlie"}, headers=auth_headers)
    client.post(
        "/api/cars",
        json={"color": "yellow", "model": "hatch", "owner_id": 1},
        headers=auth_headers,
    )
    client.post(
        "/api/cars",
        json={"color": "blue", "model": "sedan", "owner_id": 1},
        headers=auth_headers,
    )

    response = client.get("/api/cars", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 2


def test_add_fourth_car(client, auth_headers):
    client.post("/api/car_owners", json={"name": "David"}, headers=auth_headers)
    for i in range(3):
        client.post(
            "/api/cars",
            json={"color": "blue", "model": "sedan", "owner_id": 1},
            headers=auth_headers,
        )

    response = client.post(
        "/api/cars",
        json={"color": "blue", "model": "sedan", "owner_id": 1},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Owner already has 3 cars" in response.json["message"]


def test_add_invalid_color(client, auth_headers):
    client.post("/api/car_owners", json={"name": "Eve"}, headers=auth_headers)
    response = client.post(
        "/api/cars",
        json={"color": "red", "model": "sedan", "owner_id": 1},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Invalid color" in response.json["message"]


def test_add_invalid_model(client, auth_headers):
    client.post("/api/car_owners", json={"name": "Frank"}, headers=auth_headers)
    response = client.post(
        "/api/cars",
        json={"color": "blue", "model": "suv", "owner_id": 1},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Invalid model" in response.json["message"]
