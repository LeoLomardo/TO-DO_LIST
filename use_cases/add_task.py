from domain.task import Task
from domain.repositories.task_repository import TaskRepository


class AddTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task: Task) -> Task:
        return self.repo.add(task)
