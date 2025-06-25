from flask import Flask
from infra.db import Database
from infra.task_repository_sqlite import SQLiteTaskRepository
from infra.user_repository_sqlite import SQLiteUserRepository
from use_cases.add_task import AddTaskUseCase
from use_cases.list_tasks import ListTasksUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.toggle_task_status import ToggleTaskStatusUseCase
from use_cases.add_user import AddUserUseCase
from use_cases.find_user_by_email import FindUserByEmailUseCase
from app.routes.tasks import create_task_blueprint
from app.routes.pages import create_page_blueprint
from app.routes.auth import create_auth_blueprint


def create_app(db_path: str = 'app.db') -> Flask:
    app = Flask(__name__)
    app.secret_key = 'secret'
    db = Database(db_path)
    task_repo = SQLiteTaskRepository(db)
    user_repo = SQLiteUserRepository(db)

    add_uc = AddTaskUseCase(task_repo)
    list_uc = ListTasksUseCase(task_repo)
    delete_uc = DeleteTaskUseCase(task_repo)
    toggle_uc = ToggleTaskStatusUseCase(task_repo)

    add_user_uc = AddUserUseCase(user_repo)
    find_user_uc = FindUserByEmailUseCase(user_repo)

    task_bp = create_task_blueprint(add_uc, list_uc, delete_uc, toggle_uc)
    page_bp = create_page_blueprint(add_uc, list_uc, delete_uc, toggle_uc)
    auth_bp = create_auth_blueprint(add_user_uc, find_user_uc)
    app.register_blueprint(task_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
