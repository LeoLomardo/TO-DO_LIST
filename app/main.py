import sys
import os
# Adicione o diretório raiz ao path do Python no início do arquivo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template
from use_cases.task_use_case import TaskUseCase
from infra.repositories.task_repository_sqlite import TaskRepository
from app.routes.task_routes import task_bp

app = Flask(__name__)

# Registre o blueprint
app.register_blueprint(task_bp, url_prefix='/api/tasks')

# Setup do repositório e caso de uso
repo = TaskRepository()
use_case = TaskUseCase(repo)

@app.route('/')
def index():
    tasks = use_case.get_all_tasks()  # Usando o método correto
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    # Inicialize o banco de dados usando o repositório
    repo._init_db()  # O repositório já tem o método de inicialização
    app.run(debug=True)