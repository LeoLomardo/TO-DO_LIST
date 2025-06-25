from typing import List, Optional
from domain.task import Task
from domain.repositories.task_repository import TaskRepository
from infra.db import Database



class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db: Database):
        self.db = db

    def add(self, task: Task) -> Task:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, user_id, completed) '
            'VALUES (?, ?, ?, ?)',
            (task.title, task.description, task.user_id, int(task.completed))
        )
        conn.commit()
        task.id = cursor.lastrowid
        conn.close()
        return task

    def list(self) -> List[Task]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(
            'SELECT id, title, description, user_id, completed FROM tasks'
        ).fetchall()
        tasks = [
            Task(
                id=row[0],
                title=row[1],
                description=row[2],
                user_id=row[3],
                completed=bool(row[4]),
            )
            for row in rows
        ]
        conn.close()
        return tasks

    def list_by_user(self, user_id: int) -> List[Task]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(
            'SELECT id, title, description, user_id, completed FROM tasks '
            'WHERE user_id=?',
            (user_id,),
        ).fetchall()
        tasks = [
            Task(
                id=row[0],
                title=row[1],
                description=row[2],
                user_id=row[3],
                completed=bool(row[4]),
            )
            for row in rows
        ]
        conn.close()
        return tasks

    def delete(self, task_id: int) -> None:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()
        conn.close()

    def get(self, task_id: int) -> Optional[Task]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT id, title, description, user_id, completed FROM tasks '
            'WHERE id=?',
            (task_id,),
        ).fetchone()
        conn.close()
        if row:
            return Task(
                id=row[0],
                title=row[1],
                description=row[2],
                user_id=row[3],
                completed=bool(row[4]),
            )
        return None

    def update(self, task: Task) -> Task:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET title=?, description=?, user_id=?, completed=? '
            'WHERE id=?',
            (task.title, task.description, task.user_id, int(task.completed), task.id),
        )
        conn.commit()
        conn.close()
        return task
