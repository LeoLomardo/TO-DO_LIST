from typing import List, Optional
from domain.task import Task
from domain.repositories.task_repository import TaskRepository


class ListTasksUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, user_id: Optional[int] = None) -> List[Task]:
        if user_id is None:
            return self.repo.list()
        return self.repo.list_by_user(user_id)
