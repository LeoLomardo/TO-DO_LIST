from domain.repositories.user_repository import UserRepository
import pytest
from domain.task import Task
from domain.user import User
from use_cases.add_task import AddTaskUseCase
from use_cases.list_tasks import ListTasksUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.toggle_task_status import ToggleTaskStatusUseCase
from use_cases.add_user import AddUserUseCase
from use_cases.find_user_by_email import FindUserByEmailUseCase
from domain.repositories.task_repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks = []
        self.counter = 1

    def add(self, task: Task) -> Task:
        task.id = self.counter
        self.counter += 1
        self.tasks.append(task)
        return task

    def list(self):
        return list(self.tasks)

    def list_by_user(self, user_id: int):
        return [t for t in self.tasks if t.user_id == user_id]

    def delete(self, task_id: int) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get(self, task_id: int):
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def update(self, task: Task) -> Task:
        for idx, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[idx] = task
                break
        return task

class InMemoryUserRepository:
    def __init__(self):
        self.users = []
        self.counter = 1

    def add(self, user: User):
        user.id = self.counter
        self.counter += 1
        self.users.append(user)
        return user

    def get_by_email(self, email):
        for u in self.users:
            if u.email == email:
                return u
        return None

# ---- TESTES DE TASKS ----

def test_add_and_list_tasks():
    repo = InMemoryTaskRepository()
    add_use_case = AddTaskUseCase(repo)
    list_use_case = ListTasksUseCase(repo)

    task = Task(id=0, title='Test', description='Desc', user_id=1)
    add_use_case.execute(task)

    tasks = list_use_case.execute()
    assert len(tasks) == 1
    assert tasks[0].title == 'Test'

def test_delete_task():
    repo = InMemoryTaskRepository()
    add_use_case = AddTaskUseCase(repo)
    delete_use_case = DeleteTaskUseCase(repo)
    list_use_case = ListTasksUseCase(repo)

    task1 = add_use_case.execute(Task(id=0, title='t1', description='', user_id=1))
    task2 = add_use_case.execute(Task(id=0, title='t2', description='', user_id=1))

    delete_use_case.execute(task1.id)
    tasks = list_use_case.execute()
    assert len(tasks) == 1
    assert tasks[0].id == task2.id

def test_toggle_task_status():
    repo = InMemoryTaskRepository()
    add_uc = AddTaskUseCase(repo)
    toggle_uc = ToggleTaskStatusUseCase(repo)

    task = add_uc.execute(Task(id=0, title='t', description='', user_id=1))
    assert not task.completed

    toggled = toggle_uc.execute(task.id)
    assert toggled.completed

def test_list_by_user():
    repo = InMemoryTaskRepository()
    add_uc = AddTaskUseCase(repo)
    add_uc.execute(Task(id=0, title='t1', description='', user_id=1))
    add_uc.execute(Task(id=0, title='t2', description='', user_id=2))
    add_uc.execute(Task(id=0, title='t3', description='', user_id=1))

    tasks_user1 = repo.list_by_user(1)
    tasks_user2 = repo.list_by_user(2)
    assert len(tasks_user1) == 2
    assert all(t.user_id == 1 for t in tasks_user1)
    assert len(tasks_user2) == 1
    assert tasks_user2[0].user_id == 2

def test_update_task():
    repo = InMemoryTaskRepository()
    add_uc = AddTaskUseCase(repo)
    task = add_uc.execute(Task(id=0, title='old', description='', user_id=1))
    task.title = 'new'
    repo.update(task)
    updated = repo.get(task.id)
    assert updated.title == 'new'

def test_get_task():
    repo = InMemoryTaskRepository()
    add_uc = AddTaskUseCase(repo)
    task = add_uc.execute(Task(id=0, title='findme', description='', user_id=1))
    found = repo.get(task.id)
    not_found = repo.get(999)
    assert found is not None
    assert found.title == 'findme'
    assert not_found is None

def test_delete_nonexistent_task():
    repo = InMemoryTaskRepository()
    add_uc = AddTaskUseCase(repo)
    add_uc.execute(Task(id=0, title='t', description='', user_id=1))
    repo.delete(999)  # Should not raise
    assert len(repo.list()) == 1

def test_toggle_nonexistent_task():
    repo = InMemoryTaskRepository()
    toggle_uc = ToggleTaskStatusUseCase(repo)
    with pytest.raises(ValueError, match="Task not found"):
        toggle_uc.execute(999)

# ---- TESTES DE USUÁRIO ----

def test_add_user():
    repo = InMemoryUserRepository()
    add_uc = AddUserUseCase(repo)
    user = User(id=0, name='Test', email='test@email.com')
    added = add_uc.execute(user)
    assert added.id == 1
    assert added.name == 'Test'
    assert repo.get_by_email('test@email.com') is not None

def test_find_user_by_email():
    repo = InMemoryUserRepository()
    add_uc = AddUserUseCase(repo)
    find_uc = FindUserByEmailUseCase(repo)
    user = User(id=0, name='Test', email='test@email.com')
    add_uc.execute(user)
    found = find_uc.execute('test@email.com')
    assert found is not None
    assert found.name == 'Test'
    assert found.email == 'test@email.com'
