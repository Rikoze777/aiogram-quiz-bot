import logging
import asyncio
import handlers
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env


logging.basicConfig(level=logging.INFO)


async def main():
    env = Env()
    env.read_env()
    API_TOKEN = env.str("API_TOKEN")
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    dp.include_routers(handlers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
