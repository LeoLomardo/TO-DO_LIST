import pytest
from unittest.mock import Mock
from use_cases.task_use_case import TaskUseCase
from domain.task import Task

def test_create_task():
    repo = Mock()
    use_case = TaskUseCase(repo)
    repo.create.return_value = Task(1, "Test Task", "Description", user_id=1)
    
    task = use_case.create_task("Test Task", "Description", user_id=1)
    assert task.id == 1
    assert task.title == "Test Task"
    repo.create.assert_called_once_with("Test Task", "Description", 1)

def test_get_all_tasks():
    repo = Mock()
    use_case = TaskUseCase(repo)
    repo.get_all.return_value = [Task(1, "Task 1"), Task(2, "Task 2")]
    
    tasks = use_case.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    repo.get_all.assert_called_once()