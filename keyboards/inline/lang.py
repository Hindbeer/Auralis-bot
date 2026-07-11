from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import LanguageCallback


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    languages = [
        ("🇷🇺 Русский", "ru"),
        ("🇬🇧 English", "en"),
    ]
    for label, locale in languages:
        builder.button(
            text=label,
            callback_data=LanguageCallback(locale=locale),
            style=ButtonStyle.SUCCESS,
        )
    builder.adjust(1)
    return builder.as_markup()
