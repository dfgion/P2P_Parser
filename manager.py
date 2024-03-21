import asyncio

from core.config.cfg import bot, dp
from core.handlers import basic, subscriptions, profile, payments, scanner
from core.config.cfg import set_commands
from core.middlewares.basic import SubAccessMiddleware
from core.utils.redis import set_values

from db.db_config import async_start, async_session
from db.db_func import insert_basic

async def on_startup(dispatcher):
    print('Бот Запущен')

async def async_main() -> None:
    await async_start()
    await insert_basic(async_session=async_session)
    await set_values(async_session=async_session)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    basic.router.callback_query.middleware(SubAccessMiddleware())
    dp.include_routers(basic.router, subscriptions.router, profile.router, payments.router, scanner.router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(async_main())