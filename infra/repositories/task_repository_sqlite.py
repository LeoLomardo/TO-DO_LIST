from domain.task import Task
from infra.db.database import get_connection

class TaskRepository:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Initialize the database, creating users and tasks tables."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Create tasks table with foreign key to users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

    def create(self, title, description, user_id=None):
        """Create a new task with an optional user_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)",
            (title, description, user_id)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return Task(task_id, title, description, user_id=user_id)

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed, user_id FROM tasks")
        rows = cursor.fetchall()
        conn.close()
        return [Task(id=row[0], title=row[1], description=row[2], completed=bool(row[3]), user_id=row[4]) for row in rows]

    def get_by_id(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, completed, user_id FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return Task(id=row[0], title=row[1], description=row[2], completed=bool(row[3]), user_id=row[4]) if row else None

    def update(self, task_id, title=None, description=None, completed=None, user_id=None):
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
        if user_id is not None:
            fields.append("user_id = ?")
            values.append(user_id)

        if not fields:
            conn.close()
            return self.get_by_id(task_id)

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
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return affected_rows > 0