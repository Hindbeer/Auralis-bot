from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ButtonStyle

audio = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🌅 Обложка",
                style=ButtonStyle.PRIMARY,
                callback_data="audio_cover",
            )
        ],
        [
            InlineKeyboardButton(
                text="👤 Исполнитель",
                style=ButtonStyle.PRIMARY,
                callback_data="audio_artist",
            ),
            InlineKeyboardButton(
                text="📝 Название",
                style=ButtonStyle.PRIMARY,
                callback_data="audio_title",
            ),
        ],
        [
            InlineKeyboardButton(
                text="💾 Сохранить",
                style=ButtonStyle.SUCCESS,
                callback_data="audio_save",
            )
        ],
    ]
)
