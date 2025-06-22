from domain.task import Task

class TaskUseCase:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title, description, due_date=None, priority="media"):
        return self.repository.create(title, description, due_date, priority)

    def get_all_tasks(self):
        return self.repository.get_all()

    def update_task(self, task_id, title=None, description=None, due_date=None, priority=None, completed=None):
        return self.repository.update(task_id, title, description, due_date, priority, completed)

    def delete_task(self, task_id):
        return self.repository.delete(task_id)
