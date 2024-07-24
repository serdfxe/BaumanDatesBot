from aiogram import Bot, Router
from aiogram.types import Message
from pythondi import inject

from app.models.user.repository import UserRepo
from utils.db.uow import UOW

start_router = Router(name="start")

@start_router.message()
@inject()
async def start_message_handler(message: Message, repo: UserRepo, uow: UOW):
    try:
        if message.from_user.id not in [i.id for i in await repo.get_users()]:
            async with uow:
                await repo.create_user(
                    id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    role="user",
                    banned=False,
                )
                
                await uow.commit()
    except Exception as ex:
        await message.answer("Не удалось создать пользователя.")
        raise ex
    else:
        await message.answer("Yeees!")
        await message.answer(str([i.id for i in await repo.get_users()]))
