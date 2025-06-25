from abc import ABC, abstractmethod
from typing import List, Optional
from domain.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        pass

    @abstractmethod
    def list(self) -> List[Task]:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass

    @abstractmethod
    def get(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass
