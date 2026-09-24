import os

import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

TODO_SERVICE_URL = os.getenv(
    "TODO_SERVICE_URL",
    "http://localhost:5001"
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    response = requests.get(
        f"{TODO_SERVICE_URL}/todos",
        timeout=5,
    )

    return jsonify(response.json()), response.status_code


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    response = requests.get(
        f"{TODO_SERVICE_URL}/todos/{todo_id}",
        timeout=5,
    )

    return jsonify(response.json()), response.status_code


@app.route("/todos", methods=["POST"])
def create_todo():
    response = requests.post(
        f"{TODO_SERVICE_URL}/todos",
        json=request.get_json(),
        timeout=5,
    )

    return jsonify(response.json()), response.status_code


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    response = requests.put(
        f"{TODO_SERVICE_URL}/todos/{todo_id}",
        json=request.get_json(),
        timeout=5,
    )

    return jsonify(response.json()), response.status_code


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    response = requests.delete(
        f"{TODO_SERVICE_URL}/todos/{todo_id}",
        timeout=5,
    )

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
