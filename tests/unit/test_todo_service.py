import pytest

from todo_service.app import app, db, Todo


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_todo(client):
    response = client.post(
        "/todos",
        json={"text": "Learn microservices"},
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["text"] == "Learn microservices"
    assert data["complete"] is False
    assert "id" in data


def test_get_todos(client):
    client.post(
        "/todos",
        json={"text": "First task"},
    )

    client.post(
        "/todos",
        json={"text": "Second task"},
    )

    response = client.get("/todos")

    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_todo(client):
    create_response = client.post(
        "/todos",
        json={"text": "Test task"},
    )

    todo_id = create_response.json["id"]

    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json["id"] == todo_id
    assert response.json["text"] == "Test task"


def test_get_missing_todo(client):
    response = client.get("/todos/9999")

    assert response.status_code == 404
    assert response.json["error"] == "Todo not found"


def test_update_todo(client):
    create_response = client.post(
        "/todos",
        json={"text": "Old task"},
    )

    todo_id = create_response.json["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={
            "text": "Updated task",
            "complete": True,
        },
    )

    assert response.status_code == 200
    assert response.json["text"] == "Updated task"
    assert response.json["complete"] is True


def test_delete_todo(client):
    create_response = client.post(
        "/todos",
        json={"text": "Delete me"},
    )

    todo_id = create_response.json["id"]

    response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 200

    get_response = client.get(f"/todos/{todo_id}")

    assert get_response.status_code == 404


def test_create_todo_without_text(client):
    response = client.post(
        "/todos",
        json={},
    )

    assert response.status_code == 400
