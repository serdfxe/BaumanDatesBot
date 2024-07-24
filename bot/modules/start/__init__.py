from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from app.exceptions import AlreadyExists, InvalidConfirmationCodeError, NotValidEmail
from app.models.user.schema import RegisterUserSchema
from app.services.profile import ProfileService


start_router = Router(name="start")


class EmailStates(StatesGroup):
    email = State()
    code = State()
    
class ProfileStates(StatesGroup):
    name = State()
    age = State()
    description = State()
    photo = State()


@start_router.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    service = ProfileService()
    
    user = message.from_user
    
    try:
        if not await service.registered(message.from_user.id):
            await service.register(
                RegisterUserSchema(
                    id=user.id, 
                    first_name=user.first_name, 
                    last_name=user.last_name, 
                    username=user.username
                )
            )
    except Exception as ex:
        await message.answer("Что-то пошло не так ;(")
        raise ex
    else:
        await message.answer(
            """Добро пожаловать в Bauman.Dates!
            
Здесь сутденты Бауманки могут знакомится и общаться
            
Давай начнём заполнять твою анкету. Но для начала надо подтвердить, что ты из Бауманки. Пришли корпоративную почту. Например: bobis@student.bmstu.ru
            """
        )
        
        await state.set_state(EmailStates.email)
        

@start_router.message(EmailStates.email)
async def email_handler(message: Message, state: EmailStates):
    service = ProfileService()
    
    try:
        await service.process_email(message.from_user.id, message.text)
    except AlreadyExists:
        await message.answer("К сожалению пользователь с такой почтой уже существует. Попробуйте ввести дургую почту.")
    except NotValidEmail:
        await message.answer("Вы ввели почту не правильно. Убедитесь, что она выглядит как: bobis@student.bmstu.ru")
    else:
        await message.answer("Отлично. Мы отправили вам код на почту. Отправьте его нам для её подтверждения.")

        await state.update_data(email=message.text)
        await state.set_state(EmailStates.code)
        
    
@start_router.message(EmailStates.code)
async def email_confirmation_code_handler(message: Message, state: EmailStates):
    service = ProfileService()
    
    data = await state.get_data()
    
    try:
        await service.confirm_email(message.from_user.id, data['email'], message.text)
    except InvalidConfirmationCodeError:
        await message.answer("Неверный код. Попробуйте ещё раз.")
    else:
        await message.answer("Отлично! Вы подтвердили почту.\n\nТеперь давай заполним твою анкету.")
