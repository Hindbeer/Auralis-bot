from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ButtonStyle

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⛔️ Отмена",
                style=ButtonStyle.DANGER,
                callback_data="cancel_edit",
            )
        ],
    ]
)
