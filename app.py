# FR9 &FR10 & FR11 & REST API 



from flask import Flask, request, jsonify
from service import TaskService
from storage import FileManager
from models import Task
import atexit

app = Flask(__name__)
service = TaskService()
storage = FileManager()

# Load saved tasks (FR10)
saved_tasks = storage.load_tasks()
for t in saved_tasks:
    task = Task(t["title"], t["description"], t["deadline"], t["priority"])
    task.status = t["status"]
    service.tasks.append(task)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    title = data.get("title")
    description = data.get("description")
    deadline = data.get("deadline")
    priority = data.get("priority")

    if not title or not deadline or not priority:
        return jsonify({"error": "Missing required fields"}), 400

    if priority.lower() not in ["high", "medium", "low"]:
        return jsonify({"error": "Invalid priority value"}), 400

    priority = priority.capitalize()

    task = Task(title, description, deadline, priority)
    service.add_task(task)

    return jsonify(task.to_dict()), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([t.to_dict() for t in service.list_tasks()])

@app.route("/tasks/<int:index>", methods=["PUT"])
def update_task(index):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    task = service.edit_task(index, **data)
    return jsonify(task.to_dict())


@app.route("/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    service.delete_task(index)
    return "", 204

@app.route("/tasks/<int:index>/complete", methods=["GET"])
def complete_task(index):
    service.mark_completed(index)
    return jsonify(service.tasks[index].to_dict())

@app.route("/tasks/sort/<type>", methods=["GET"])
def sort_tasks(type):
    if type == "deadline":
        service.sort_by_deadline()
    elif type == "priority":
        service.sort_by_priority()
    return jsonify([t.to_dict() for t in service.tasks])

@app.route("/tasks/filter/<type>", methods=["GET"])
def filter_tasks(type):
    tasks = service.filter_tasks(type)
    return jsonify([t.to_dict() for t in tasks])

@app.route("/tasks/export", methods=["GET"])
def export_tasks():
    with open("exported_tasks.txt", "w", encoding="utf-8") as f:
        for t in service.tasks:
            f.write(str(t.to_dict()) + "\n")
    return {"message": "Tasks exported successfully"}

# Save automatically on exit (FR9)
@atexit.register
def save_on_exit():
    storage.save_tasks(service.tasks)

if __name__ == "__main__":
    app.run(debug=True)
