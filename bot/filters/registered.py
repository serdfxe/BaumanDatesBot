from aiogram.filters import Filter
from aiogram.types import Message

from app.services.profile import ProfileService

class Registered(Filter):
    async def __call__(self, message: Message) -> bool:
        return ProfileService().registered(message.from_user.id)