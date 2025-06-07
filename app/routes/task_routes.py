from flask import Blueprint, jsonify, request
from use_cases.task_use_case import TaskUseCase
from infra.repositories.task_repository_sqlite import TaskRepository

task_bp = Blueprint("task", __name__)
repo = TaskRepository()
use_case = TaskUseCase(repo)


@task_bp.route("/", methods=["GET"])
def get_tasks():
    return jsonify([task.to_dict() for task in use_case.get_all_tasks()])

@task_bp.route("/", methods=["POST"])
def add_task():
    data = request.json
    task = use_case.create_task(data["title"], data.get("description", ""))
    return jsonify(task.to_dict()), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    updated_task = use_case.update_task(
        task_id,
        title=data.get("title"),
        description=data.get("description"),
        completed=data.get("completed")
    )
    if updated_task:
        return jsonify(updated_task.to_dict())
    return jsonify({"error": "Tarefa não encontrada"}), 404

@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    success = use_case.delete_task(task_id)
    return ("", 204) if success else ({"error": "Tarefa não encontrada"}, 404)

    