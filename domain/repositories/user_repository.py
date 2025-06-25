from abc import ABC, abstractmethod
from typing import List, Optional
from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
