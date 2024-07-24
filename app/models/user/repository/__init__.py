from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, func, select, update

from app.models.user.domain import MailConfimationCode, User

from utils.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = session

    @abstractmethod
    async def create(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool, email: str, verified: bool) -> User:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass
    
    @abstractmethod
    async def user_exists(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def email_exists(self, email: str) -> None:
        ...
    
    @abstractmethod
    async def set_verified_email(self, id: int, email: str) -> None:
        ...
        
    @abstractmethod
    async def process_email(self, id: int, email: str, code: str) -> None:
        ...
        
    @abstractmethod
    async def get_email_confirmation_code(self, id: int, email: str) -> None:
        ...


class AlchemyUserRepo(UserRepo):
    async def create(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool, email: str, verified: bool) -> User:
        user = User(id=id, first_name=first_name, last_name=last_name, username=username, role=role, banned=banned, email=email, verified=verified)

        await self.save(user)

    async def get_users(self) -> List[User]:
        query = await self.session.execute(select(User))

        return query.scalars().all()

    async def save(self, user: User) -> User:
        self.session.add(user)
        
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)

    async def user_exists(self, id: int) -> bool:
        query = await self.session.execute(select(func.count(User.id)).where(User.id == id))
        count = query.scalar()
        
        return count > 0
    
    async def email_exists(self, email: str) -> None:
        query = await self.session.execute(select(func.count(User.email)).where(User.email == email))
        count = query.scalar()
        
        return count > 0
    
    async def set_verified_email(self, id: int, email: str) -> None:
        await self.session.execute(
            update(User).where(User.id == id).values(email=email, verified=True)
        )
        
    async def process_email(self, id: int, email: str, code: str) -> None:
        mail_confirmation_obj = MailConfimationCode(user_id=id, email=email, code=code)
        
        await self.save(mail_confirmation_obj)
        
    async def get_email_confirmation_code(self, id: int, email: str) -> str:
        query = await self.session.execute(
            select(MailConfimationCode).where(MailConfimationCode.user_id == id).where(MailConfimationCode.email == email)
        )

        return query.scalar().code