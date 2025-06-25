from domain.repositories.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task_id: int) -> None:
        self.repo.delete(task_id)
