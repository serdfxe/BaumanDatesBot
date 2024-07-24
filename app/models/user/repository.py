from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, select

from app.models.user import User

from utils.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = session

    @abstractmethod
    async def create_user(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool) -> User:
        pass

    @abstractmethod
    async def get_users(self) -> List[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class AlchemyUserRepo(UserRepo):
    async def create_user(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool) -> User:
        user = User(id=id, first_name=first_name, last_name=last_name, username=username, role=role, banned=banned)

        await self.save(user)


    async def get_users(self) -> List[User]:
        query = await self.session.execute(select(User))

        return query.scalars().all()


    async def save(self, user: User) -> User:
        self.session.add(user)
        
        return user


    async def delete(self, user: User) -> None:
        await self.session.delete(user)
