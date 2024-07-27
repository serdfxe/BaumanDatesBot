from pythondi import Provider, configure

from app.models.profile.repository import ProfileRepo, AlchemyProfileRepo
from app.models.request.repository import AlchemyRequestRepo, RequestRepo
from app.models.user.repository import AlchemyUserRepo, UserRepo

from utils.db.uow import UOW, AlchemyUOW


def init_di():
    provider = Provider()

    provider.bind(UOW, AlchemyUOW)  

    provider.bind(UserRepo, AlchemyUserRepo)

    provider.bind(ProfileRepo, AlchemyProfileRepo)
    
    provider.bind(RequestRepo, AlchemyRequestRepo)

    configure(provider=provider)
