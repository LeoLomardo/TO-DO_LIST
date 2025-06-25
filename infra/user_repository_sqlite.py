from typing import List, Optional
from domain.user import User
from domain.repositories.user_repository import UserRepository
from infra.db import Database


class SQLiteUserRepository(UserRepository):
    def __init__(self, db: Database):
        self.db = db

    def add(self, user: User) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (user.name, user.email),
        )
        conn.commit()
        user.id = cursor.lastrowid
        conn.close()
        return user

    def list(self) -> List[User]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(
            'SELECT id, name, email FROM users'
        ).fetchall()
        users = [
            User(id=row[0], name=row[1], email=row[2])
            for row in rows
        ]
        conn.close()
        return users

    def get(self, user_id: int) -> Optional[User]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT id, name, email FROM users WHERE id=?',
            (user_id,),
        ).fetchone()
        conn.close()
        if row:
            return User(id=row[0], name=row[1], email=row[2])
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT id, name, email FROM users WHERE email=?',
            (email,),
        ).fetchone()
        conn.close()
        if row:
            return User(id=row[0], name=row[1], email=row[2])
        return None
