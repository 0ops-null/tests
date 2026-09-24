from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "complete": self.complete,
        }


with app.app_context():
    db.create_all()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify(todo.to_dict()), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    if not data or not data.get("text"):
        return jsonify({"error": "text is required"}), 400

    todo = Todo(
        text=data["text"],
        complete=data.get("complete", False),
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()

    if "text" in data:
        todo.text = data["text"]

    if "complete" in data:
        todo.complete = data["complete"]

    db.session.commit()

    return jsonify(todo.to_dict()), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
