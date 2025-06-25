from domain.repositories.task_repository import TaskRepository
from domain.task import Task


class ToggleTaskStatusUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task_id: int) -> Task:
        task = self.repo.get(task_id)
        if not task:
            raise ValueError("Task not found")
        task.completed = not task.completed
        return self.repo.update(task)
