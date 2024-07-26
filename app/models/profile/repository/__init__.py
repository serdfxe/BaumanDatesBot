from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, select

from app.models.profile.domain import Profile

from utils.db.session import Session
from utils.deb import p


class ProfileRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = Session()

    @abstractmethod
    def create(self,  user_id: int, name: str, age: int, sex: str, description: str, photo: str) -> Profile:
        pass

    @abstractmethod
    def get_all(self) -> List[Profile]:
        pass

    @abstractmethod
    def save(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    def delete(self, profile: Profile) -> None:
        pass


class AlchemyProfileRepo(ProfileRepo):
    def create(self,  user_id: int, name: str, age: int, sex: str, description: str, photo: str) -> Profile:
        p(11)
        profile = Profile(user_id=user_id, name=name, age=age,  sex = sex,  description=description, photo=photo)
        p(22)

        self.save(profile)


    def get_profiles(self) -> List[Profile]:
        query = self.session.execute(select(Profile))

        return query.scalars().all()


    def save(self, profile: Profile) -> Profile:
        self.session.add(profile)
        
        return profile


    def delete(self, profile: Profile) -> None:
        self.session.delete(profile)
