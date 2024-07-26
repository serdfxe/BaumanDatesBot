from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, func, select, update

from app.models.user.domain import MailConfimationCode, User

from utils.db.session import Session
from utils.deb import p


class UserRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = Session()

    @abstractmethod
    def create(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool, email: str, verified: bool) -> User:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
    
    @abstractmethod
    def user_exists(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def email_exists(self, email: str) -> None:
        ...
    
    @abstractmethod
    def set_verified_email(self, id: int, email: str) -> None:
        ...
        
    @abstractmethod
    def process_email(self, id: int, email: str, code: str) -> None:
        ...
        
    @abstractmethod
    def get_email_confirmation_code(self, id: int, email: str) -> None:
        ...


class AlchemyUserRepo(UserRepo):
    def create(self,  id: int, first_name: str, last_name: str, username: str, role: str, banned: bool, email: str, verified: bool) -> User:
        user = User(id=id, first_name=first_name, last_name=last_name, username=username, role=role, banned=banned, email=email, verified=verified)

        self.save(user)

    def get_users(self) -> List[User]:
        query = self.session.execute(select(User))

        return query.scalars().all()

    def save(self, user: User) -> User:
        self.session.add(user)
        
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)

    def user_exists(self, id: int) -> bool:
        p("AAAAAAAAAAAAAAAA")
        return self.session.query(User).filter_by(id=id).first()
    
    def email_exists(self, email: str) -> None:
        query = self.session.execute(select(func.count(User.email)).where(User.email == email))
        count = query.scalar()
        
        return count > 0
    
    def set_verified_email(self, id: int, email: str) -> None:
        self.session.execute(
            update(User).where(User.id == id).values(email=email, verified=True)
        )
        
    def process_email(self, id: int, email: str, code: str) -> None:
        mail_confirmation_obj = MailConfimationCode(user_id=id, email=email, code=code)
        
        self.save(mail_confirmation_obj)
        
    def get_email_confirmation_code(self, id: int, email: str) -> str:
        query = self.session.execute(
            select(MailConfimationCode).where(MailConfimationCode.user_id == id).where(MailConfimationCode.email == email)
        )

        return query.scalar().code