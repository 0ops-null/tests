from unittest.mock import Mock, patch

from gateway_service.app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


@patch("gateway_service.app.requests.get")
def test_get_todos(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "text": "Test task",
            "complete": False,
        }
    ]

    mock_get.return_value = mock_response

    client = app.test_client()

    response = client.get("/todos")

    assert response.status_code == 200

    assert response.json == [
        {
            "id": 1,
            "text": "Test task",
            "complete": False,
        }
    ]

    mock_get.assert_called_once()


@patch("gateway_service.app.requests.post")
def test_create_todo(mock_post):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 1,
        "text": "New task",
        "complete": False,
    }

    mock_post.return_value = mock_response

    client = app.test_client()

    response = client.post(
        "/todos",
        json={"text": "New task"},
    )

    assert response.status_code == 201

    assert response.json["text"] == "New task"

    mock_post.assert_called_once()
