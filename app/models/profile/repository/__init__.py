from abc import ABCMeta, abstractmethod
from typing import List

from sqlalchemy import delete, func, not_, select

from app.models.profile.domain import Profile, ViewedProfile

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
    
    @abstractmethod
    def get_random_unviewed_profile(self, observer_id: int) -> Profile | None:
        pass
    
    @abstractmethod
    def set_profile_viewed(self, observer_id: int, target_id: int, status: bool) -> None:
        pass

    @abstractmethod
    def get_match(self, id_1: int, id_2: int) -> bool:
        pass



class AlchemyProfileRepo(ProfileRepo):
    def create(self,  user_id: int, name: str, age: int, sex: str, description: str, photo: str) -> Profile:
        profile = Profile(user_id=user_id, name=name, age=age,  sex = sex,  description=description, photo=photo)

        return self.save(profile)

    def get_profiles(self) -> List[Profile]:
        query = self.session.execute(select(Profile))

        return query.scalars().all()

    def save(self, profile: Profile) -> Profile:
        self.session.add(profile)
        
        return profile

    def delete(self, profile: Profile) -> None:
        self.session.delete(profile)
    
    def get_random_unviewed_profile(self, observer_id: int) -> Profile | None:
        subquery = (
            select(ViewedProfile.target_id)
            .filter(ViewedProfile.observer_id == observer_id)
        ).subquery()

        random_profile = (
            select(Profile)
            .filter(not_(Profile.user_id.in_(subquery)))
            .order_by(func.random())
            .limit(1)
        )

        return self.session.execute(random_profile).scalar_one_or_none()
    
    def set_profile_viewed(self, observer_id: int, target_id: int, status: bool) -> None:
        obj = ViewedProfile(observer_id=observer_id, target_id=target_id, status=status)

        self.save(obj)

    def get_match(self, id_1: int, id_2: int) -> bool:
        m1 = self.session.execute(select(ViewedProfile).filter_by(target_id=id_1, observer_id=id_2, status=True)).scalar_one_or_none()
        m2 = self.session.execute(select(ViewedProfile).filter_by(target_id=id_2, observer_id=id_1, status=True)).scalar_one_or_none()

        return m1 and m2