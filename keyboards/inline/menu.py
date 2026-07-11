from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext


def get_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=i18n("bttn-cancel"),
        callback_data="cancel_edit",
        style=ButtonStyle.DANGER,
    )
    builder.adjust(1)
    return builder.as_markup()
