from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, select

from app.models.request.domain import Request

from utils.db.session import Session
from utils.deb import p


class RequestRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = Session()

    @abstractmethod
    def create(self, user_id: int, request: str) -> Request:
        pass

    @abstractmethod
    def get_all(self) -> List[Request]:
        pass

    @abstractmethod
    def save(self, request: Request) -> Request:
        pass

    @abstractmethod
    def delete(self, request: Request) -> None:
        pass


class AlchemyRequestRepo(RequestRepo):
    def create(self, user_id: int, request: str) -> Request:
        request = Request(user_id=user_id, request=request)

        self.save(request)


    def get_requests(self) -> List[Request]:
        query = self.session.execute(select(Request))

        return query.scalars().all()


    def save(self, request: Request) -> Request:
        self.session.add(request)
        
        return request


    def delete(self, request: Request) -> None:
        self.session.delete(request)
