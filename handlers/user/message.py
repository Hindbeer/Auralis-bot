from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}! \nЯ могу изменять обложку, название и артиста в треке. Пришли мне свой трек для этого",
    )
