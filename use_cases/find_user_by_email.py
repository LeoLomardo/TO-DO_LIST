from typing import Optional
from domain.user import User
from domain.repositories.user_repository import UserRepository


class FindUserByEmailUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, email: str) -> Optional[User]:
        return self.repo.get_by_email(email)
