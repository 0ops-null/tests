import json

from jsonschema import validate

from todo_service.app import app, db


def test_todo_service_contract():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()

        response = client.post(
            "/todos",
            json={"text": "Contract test"},
        )

        assert response.status_code == 201

        todo = response.get_json()

        with open("contracts/todo_contract.json") as file:
            contract = json.load(file)

        validate(
            instance=todo,
            schema=contract,
        )

        db.session.remove()
        db.drop_all()
