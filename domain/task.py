class Task:
    def __init__(self, id, title, description="", completed=False, user_id=None):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id
        }