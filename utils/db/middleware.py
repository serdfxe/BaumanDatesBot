from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from uuid import uuid4

from utils.db import reset_session_context, set_session_context, session

class SQLAlchemyMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.session_context = None

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Генерируем уникальный идентификатор сессии
        session_id = str(uuid4())

        # Устанавливаем контекст сессии
        self.session_context = set_session_context(session_id=session_id)

        try:
            return await handler(event, data)
        finally:
            # Очищаем сессию
            await session.remove()
            # Сбрасываем контекст сессии
            reset_session_context(context=self.session_context)
