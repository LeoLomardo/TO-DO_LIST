from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str
    user_id: int
    completed: bool = False
