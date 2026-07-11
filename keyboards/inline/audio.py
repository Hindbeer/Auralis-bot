from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext


def get_audio_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=i18n("bttn-cover"),
        callback_data="audio_cover",
        style=ButtonStyle.PRIMARY,
    )
    builder.button(
        text=i18n("bttn-artist"),
        callback_data="audio_artist",
        style=ButtonStyle.PRIMARY,
    )
    builder.button(
        text=i18n("bttn-title"),
        callback_data="audio_title",
        style=ButtonStyle.PRIMARY,
    )
    builder.button(
        text=i18n("bttn-save"),
        callback_data="audio_save",
        style=ButtonStyle.SUCCESS,
    )
    builder.adjust(1, 2, 1)
    return builder.as_markup()
