from aiogram import Bot, Dispatcher

from bot.modules.start import start_router
from bot.modules.support import support_router
from bot.modules.flow import flow_router

from config import TOKEN
# from utils.db.middleware import SQLAlchemyMiddleware
from utils.di import init_di


async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    
    # dp.message.middleware(SQLAlchemyMiddleware())
    
    dp.include_routers(
        start_router, 
        support_router,
        flow_router,
    )

    init_di()

    await dp.start_polling(bot)
