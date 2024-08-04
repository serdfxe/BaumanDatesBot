from pythondi import inject

from app.models.profile.repository import ProfileRepo
from app.models.profile.schema import FlowProfileSchema
from utils.db.uow import UOW


class FlowService:
    def __init__(self):
        ...
    
    @inject()
    def get_random_unviewed_profile(self, user_id: int, repo: ProfileRepo):
        profile = repo.get_random_unviewed_profile(user_id)
        
        if profile is None:
            return None
        
        return FlowProfileSchema(user_id=profile.user_id, name=profile.name, description=profile.description)
    
    @inject()
    def set_profile_viewed(self, observer_id: int, target_id: int, status: str, repo: ProfileRepo, uow: UOW):
        with uow(repo):
            repo.set_profile_viewed(observer_id, target_id, status)
                
            try:
                uow.commit()
            except:
                ...
        
    def register_like(self, observer_id: int, target_id: int):
        self.set_profile_viewed(observer_id, target_id, True)
    
    def register_dislike(self, observer_id: int, target_id: int):
        self.set_profile_viewed(observer_id, target_id, False)

    @inject()
    def is_match(self, id_1: int, id_2: int, repo: ProfileRepo) -> bool:
        return repo.get_match(id_1, id_2) is not None