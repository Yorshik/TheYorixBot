import asyncio
import logging
import os
import sys

import aiogram
import django

__all__ = ()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/bot.log"), logging.StreamHandler(sys.stdout)],
)


async def on_startup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    import utils.db

    logging.info("bot launch started")
    await utils.db.create_superuser()
    logging.info("if superuser did not exist - created")
    logging.info("bot launch ended. Bot is working stably")


async def on_shutdown(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    logging.info("bot stopped its work")


async def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TheYorixBot.TheYorixBot.settings")
    django.setup()

    import aiogram.filters.exception
    import handlers.help
    import handlers.start
    import middlewares.user_middleware
    import utils.config

    bot = aiogram.Bot(token=utils.config.config.BOT_TOKEN)
    dp = aiogram.Dispatcher()
    router = aiogram.Router()

    dp.message.middleware(middlewares.user_middleware.UserCacheMiddleware())

    router.include_router(handlers.start.router)
    router.include_router(handlers.help.router)

    dp.include_router(router)

    await on_startup(dp, bot)
    await dp.start_polling(bot)
    await on_shutdown(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
