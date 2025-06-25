from flask import Blueprint, request, jsonify, session
from domain.task import Task
from use_cases.add_task import AddTaskUseCase
from use_cases.list_tasks import ListTasksUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.toggle_task_status import ToggleTaskStatusUseCase


def create_task_blueprint(add_uc: AddTaskUseCase,
                          list_uc: ListTasksUseCase,
                          delete_uc: DeleteTaskUseCase,
                          toggle_uc: ToggleTaskStatusUseCase) -> Blueprint:
    bp = Blueprint('tasks', __name__)

    @bp.route('/tasks', methods=['POST'])
    def add_task():
        data = request.json
        user_id = data.get('user_id') or session.get('user_id') or 1
        task = Task(id=0,
                    title=data['title'],
                    description=data.get('description', ''),
                    user_id=user_id)
        result = add_uc.execute(task)
        return jsonify({
            'id': result.id,
            'title': result.title,
            'description': result.description,
            'user_id': result.user_id,
            'completed': result.completed,
        }), 201

    @bp.route('/tasks', methods=['GET'])
    def list_tasks():
        user_id = request.args.get('user_id') or session.get('user_id')
        if user_id:
            tasks = list_uc.execute(user_id=int(user_id))
        else:
            tasks = list_uc.execute()
        return jsonify([
            {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'user_id': t.user_id,
                'completed': t.completed,
            } for t in tasks
        ])

    @bp.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id: int):
        delete_uc.execute(task_id)
        return '', 204

    @bp.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
    def toggle_task(task_id: int):
        task = toggle_uc.execute(task_id)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'user_id': task.user_id,
            'completed': task.completed,
        })

    return bp
