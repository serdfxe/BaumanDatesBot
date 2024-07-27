from aiogram import Bot, Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from app.exceptions import AlreadyExists, InvalidConfirmationCodeError, NotValidEmail
from app.models.profile.schema import FillProfileSchema
from app.models.user.schema import RegisterUserSchema
from app.services.profile import ProfileService
from utils.deb import p


start_router = Router(name="start")


class EmailStates(StatesGroup):
    email = State()
    code = State()
    
class ProfileStates(StatesGroup):
    name = State()
    age = State()
    description = State()
    photo = State()
    sex = State()


@start_router.message(Command("start"))
async def start_message_handler(message: Message, state: FSMContext):
    service = ProfileService()
    
    user = message.from_user

    
    try:
        if not service.registered(message.from_user.id):
            service.register(
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
        service.process_email(message.from_user.id, message.text)
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
        service.confirm_email(message.from_user.id, data['email'], message.text)
    except InvalidConfirmationCodeError:
        await message.answer("Неверный код. Попробуйте ещё раз.")
    else:
        await message.answer("Отлично! Вы подтвердили почту.\n\nТеперь давайте заполним вашу анкету. \n Введите ваше имя:")
        await state.set_state(ProfileStates.name)

@start_router.message(ProfileStates.name)
async def profile_name_handler(message: Message, state: ProfileStates):

    if len(message.text) > 30:
        await message.answer("Длина имени должна быть меньше 30")
        return

    await state.update_data(name=message.text)
    await state.set_state(ProfileStates.age)

    await message.answer("Введите ваш возраст:")

@start_router.message(ProfileStates.age)
async def profile_age_handler(message: Message, state: ProfileStates):

    try:
        age = int(message.text)
        if age > -1 and age <= 69:
            await state.update_data(age=age)
            await state.set_state(ProfileStates.description)
            await message.answer("Теперь введите описание для вашей анкеты.")
        else:
            raise ValueError
    except Exception:
        await message.answer("Ошибка! Возраст должен быть числом в диапазоне 0 - 69")

@start_router.message(ProfileStates.description)
async def profile_description_handler(message: Message, state: ProfileStates):

    buttons = [
        InlineKeyboardButton(text='М', callback_data='gender_Male'),
        InlineKeyboardButton(text='Ж', callback_data='gender_Female'),
        InlineKeyboardButton(text='-', callback_data='gender_None')
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons], row_width = 3)

    if len(message.text) > 250:
        await message.answer("Описание слишком длинное, пожалуйста уменьшите его ^_^")
        return
    
    await state.update_data(description = message.text)
    await state.set_state(ProfileStates.sex)
    await message.answer("Выберите ваш пол", reply_markup=keyboard)


@start_router.callback_query(lambda c: c.data.startswith('gender_'), ProfileStates.sex)
async def profile_sex_handler(callback_query: CallbackQuery, state: ProfileStates, bot: Bot):

    

    sex = callback_query.data.split("_")[1]
    await state.update_data(sex = sex)

    data = await state.get_data()

    p(data)

    ProfileService().fill_profile(callback_query.from_user.id, FillProfileSchema(**data))

    await bot.send_message(callback_query.from_user.id, "Поздравляем! Вы заполнили анкету!")

    await state.clear()
