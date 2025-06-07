from domain.task import Task
from infra.db.database import get_connection

class TaskRepository:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def create(self, title, description):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return Task(task_id, title, description)

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed FROM tasks")
        rows = cursor.fetchall()
        conn.close()
        return [Task(*row) for row in rows]

    def update(self, task_id, title=None, description=None, completed=None):
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        if title is not None:
            fields.append("title = ?")
            values.append(title)
        if description is not None:
            fields.append("description = ?")
            values.append(description)
        if completed is not None:
            fields.append("completed = ?")
            values.append(int(completed))

        values.append(task_id)

        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return self.get_by_id(task_id)

    def delete(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return True

    def get_by_id(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        return Task(*row) if row else None
