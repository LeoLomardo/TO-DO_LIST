from domain.user import User
from domain.repositories.user_repository import UserRepository


class AddUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, user: User) -> User:
        return self.repo.add(user)
