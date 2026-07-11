import asyncio
from pathlib import Path
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from config import config
from handlers import router as main_router

BASE_DIR = Path(__file__).parent


async def main() -> None:
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            link_preview_is_disabled=True,
        ),
    )

    dp = Dispatcher()

    dp.include_routers(main_router)

    i18n = I18nMiddleware(core=FluentRuntimeCore(path="locales/{locale}/LC_MESSAGES"))

    i18n.setup(dispatcher=dp)

    print(f"Loaded locales in Core: {i18n.core.locales}")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
