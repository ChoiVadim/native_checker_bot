import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.config import Config


async def main():
    print("Bot started!")
    bot = Bot(Config.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
