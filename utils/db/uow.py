from abc import ABCMeta, abstractmethod

from utils.db import session

class UOW:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = session

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def commit(self):
        pass

    async def __aenter__(self):
        self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        # await session.close()


class AlchemyUOW(UOW):
    def begin(self):
        return
        session.begin()

    async def rollback(self):
        await session.rollback()

    async def commit(self):
        await session.commit()
