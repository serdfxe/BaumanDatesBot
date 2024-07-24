from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, select

from app.models.profile.domain import Profile

from utils.db import session


class ProfileRepo:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.session = session

    @abstractmethod
    async def create(self,  id: int, first_name: str, last_name: str, profilename: str, role: str, banned: bool, email: str, verified: bool) -> Profile:
        pass

    @abstractmethod
    async def get_all(self) -> List[Profile]:
        pass

    @abstractmethod
    async def save(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    async def delete(self, profile: Profile) -> None:
        pass


class AlchemyProfileRepo(ProfileRepo):
    async def create(self,  user_id: int, name: str, description: str, age: str, photo: str) -> Profile:
        profile = Profile(user_id=user_id, name=name, age=age, photo=photo, description=description)

        await self.save(profile)


    async def get_profiles(self) -> List[Profile]:
        query = await self.session.execute(select(Profile))

        return query.scalars().all()


    async def save(self, profile: Profile) -> Profile:
        self.session.add(profile)
        
        return profile


    async def delete(self, profile: Profile) -> None:
        await self.session.delete(profile)
