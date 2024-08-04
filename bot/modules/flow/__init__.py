from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.services.flow import FlowService
from bot.filters.registered import Registered

flow_router = Router(name="flow")

class FlowStates(StatesGroup):
    waiting_for_photo = State()

@flow_router.message(Command("flow"), Registered())
async def flow_start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    profile_service = FlowService()
    
    # Получаем случайную непросмотренную анкету
    profile = profile_service.get_random_unviewed_profile(user_id)
    
    if profile:
        buttons = [
            InlineKeyboardButton(text="❌", callback_data=f"dislike_{profile.user_id}"),
            InlineKeyboardButton(text="❤️", callback_data=f"like_{profile.user_id}"),
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons], row_width = 2)

        await message.answer(
            f"ID: `{profile.user_id}`\n\n"
            f"Имя: {profile.name}\n"
            f"Описание: {profile.description}\n",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        
        await state.set_state(FlowStates.waiting_for_photo)

    else:
        await message.answer("Нет доступных анкет для просмотра.")

@flow_router.callback_query(lambda call: call.data.startswith("like_") or call.data.startswith("dislike_"))
async def handle_rating(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    profile_id = call.data.split("_")[1]

    flow_service = FlowService()

    try:
        if call.data.startswith("like_"):
            flow_service.register_like(user_id, profile_id)

            if flow_service.is_match(user_id, profile_id):
                await handle_match(call.bot, user_id, profile_id)
            else:
                await call.answer("Вы поставили лайк!")
        else:
            flow_service.register_dislike(user_id, profile_id)

            await call.answer("Вы поставили дизлайк!")
    except Exception as e:
        raise e

    # Запрашиваем следующую анкету
    profile = flow_service.get_random_unviewed_profile(user_id)
    if profile:
        buttons = [
            InlineKeyboardButton(text="❌", callback_data=f"dislike_{profile.user_id}"),
            InlineKeyboardButton(text="❤️", callback_data=f"like_{profile.user_id}"),
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons], row_width = 3)

        await call.message.edit_text(
            f"ID: `{profile.user_id}`\n\n"
            f"Имя: {profile.name}\n"
            f"Описание: {profile.description}\n",
            parse_mode='Markdown'
        )
        
        await call.message.edit_reply_markup(
            reply_markup=keyboard
        )
    else:
        await call.message.answer("Нет доступных анкет для просмотра.")


async def handle_match(bot: Bot, user_id: int, profile_id: int):
    ...