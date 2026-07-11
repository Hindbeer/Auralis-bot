import os

import music_tag
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_i18n import I18nContext

from config import config
from keyboards import inline
from utils import AudioEditStates, LanguageCallback

router = Router()
bot = Bot(config.BOT_TOKEN)


@router.callback_query(LanguageCallback.filter())
async def handle_language_change(
    query: CallbackQuery, callback_data: LanguageCallback, i18n: I18nContext
):
    await i18n.set_locale(callback_data.locale)

    await query.message.answer_photo(
        photo=FSInputFile("cat.jpg"),
        caption=i18n.get("welcome", name=query.from_user.first_name),
    )
    await query.answer()


@router.callback_query(AudioEditStates.edit, F.data == "audio_artist")
async def edit_artist(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18nContext
) -> None:
    await callback_query.message.answer(
        text=i18n("edit-artist"), reply_markup=inline.get_menu_keyboard(i18n)
    )
    await callback_query.answer()

    await state.set_state(AudioEditStates.artist)


@router.callback_query(AudioEditStates.edit, F.data == "audio_title")
async def edit_title(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18nContext
) -> None:
    await callback_query.message.answer(
        text=i18n("edit-title"), reply_markup=inline.get_menu_keyboard(i18n)
    )
    await callback_query.answer()

    await state.set_state(AudioEditStates.title)


@router.callback_query(AudioEditStates.edit, F.data == "audio_cover")
async def edit_cover(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18nContext
) -> None:
    await callback_query.message.answer(
        text=i18n("edit-cover"), reply_markup=inline.get_menu_keyboard(i18n)
    )
    await callback_query.answer()

    await state.set_state(AudioEditStates.cover)


@router.callback_query(F.data == "cancel_edit")
async def cancel(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    await callback_query.answer()

    await state.set_state(AudioEditStates.edit)


@router.callback_query(AudioEditStates.edit, F.data == "audio_save")
async def save_track(callback_query: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()

    track_file = music_tag.load_file(state_data["audio_filename"])
    track_file["artist"] = state_data["audio_artist"]
    track_file["tracktitle"] = state_data["audio_title"]

    with open(state_data["cover_filename"], "rb") as cover:
        track_file["artwork"] = cover.read()

    track_file.save()

    reply_audio = FSInputFile(
        state_data["audio_filename"], filename=state_data["audio_filename"]
    )
    reply_cover = FSInputFile(
        state_data["cover_filename"], filename=state_data["cover_filename"]
    )
    await callback_query.message.answer_audio(
        audio=reply_audio,
        thumbnail=reply_cover,
    )

    if os.path.exists(state_data["audio_filename"]):
        os.remove(state_data["audio_filename"])
    if state_data["cover_filename"] != "none-cover.jpg":
        os.remove(state_data["cover_filename"])

    await state.set_state(AudioEditStates.audio)
    await callback_query.answer()
