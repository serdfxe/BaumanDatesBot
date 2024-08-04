from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.services.support import SupportService


support_router = Router(name = "support")

class SupportRequest(StatesGroup):
    request = State()

@support_router.message(Command("support"))
async def support_message_handler(message: Message, state: FSMContext):
    await message.answer("Отправьте жалобу.")

    await state.set_state(SupportRequest.request)

@support_router.message(SupportRequest.request)
async def request_handler(message: Message, state: SupportRequest):
    request = message.text
    user = message.from_user
    service = SupportService()
    
    try:
        service.register_request(user_id = user.id, request = request)
    except Exception as ex:
        await message.answer("Иди нахуй")
        raise ex
    else:
        await message.answer("Жалоба принята в обработку!")

    await state.clear()