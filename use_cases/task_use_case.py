from domain.task import Task

class TaskUseCase:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title, description):
        return self.repository.create(title, description)

    def get_all_tasks(self):
        return self.repository.get_all()

    def update_task(self, task_id, title=None, description=None, completed=None):
        return self.repository.update(task_id, title, description, completed)

    def delete_task(self, task_id):
        return self.repository.delete(task_id)
    
    def get_tasks_by_user(self, user_id):
        return [task for task in self.repository.get_all() if task.user_id == user_id]
