
from pythondi import inject

from app.models.request.repository import RequestRepo
from utils.db.uow import UOW


class SupportService:
    def __init__(self):
        ...

    @inject()
    def register_request(self, user_id: int, request: str, repo: RequestRepo, uow: UOW):
        with uow(repo):
            repo.create(
                user_id = user_id,
                request = request 
            )
            
            uow.commit()