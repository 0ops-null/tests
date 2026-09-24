from app import app


def test_update_route():
    client = app.test_client()

    response = client.post("/update")

    assert response.status_code == 302
