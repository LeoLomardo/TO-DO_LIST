from flask import Blueprint, render_template, request, redirect, url_for, session
from domain.task import Task
from use_cases.add_task import AddTaskUseCase
from use_cases.list_tasks import ListTasksUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.toggle_task_status import ToggleTaskStatusUseCase


def create_page_blueprint(add_uc: AddTaskUseCase,
                          list_uc: ListTasksUseCase,
                          delete_uc: DeleteTaskUseCase,
                          toggle_uc: ToggleTaskStatusUseCase) -> Blueprint:
    bp = Blueprint('pages', __name__)

    @bp.route('/')
    def index():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        tasks = list_uc.execute(user_id=user_id)
        return render_template('index.html', tasks=tasks)

    @bp.route('/add', methods=['POST'])
    def add_task():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        title = request.form['title']
        description = request.form.get('description', '')
        task = Task(id=0, title=title, description=description, user_id=user_id)
        add_uc.execute(task)
        return redirect(url_for('pages.index'))

    @bp.route('/toggle/<int:task_id>', methods=['POST'])
    def toggle_task(task_id: int):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        toggle_uc.execute(task_id)
        return redirect(url_for('pages.index'))

    @bp.route('/delete/<int:task_id>', methods=['POST'])
    def delete_task(task_id: int):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        delete_uc.execute(task_id)
        return redirect(url_for('pages.index'))

    return bp
