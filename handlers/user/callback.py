import os

import music_tag
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from config import config
from keyboards import inline
from utils import AudioEditStates

router = Router()
bot = Bot(config.BOT_TOKEN)


@router.callback_query(AudioEditStates.edit, F.data == "audio_artist")
async def edit_artist(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer(
        text="Отправь имя исполнителя", reply_markup=inline.menu
    )
    await callback_query.answer()

    await state.set_state(AudioEditStates.artist)


@router.callback_query(AudioEditStates.edit, F.data == "audio_title")
async def edit_title(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer(
        text="Отправь название трека", reply_markup=inline.menu
    )
    await callback_query.answer()

    await state.set_state(AudioEditStates.title)


@router.callback_query(AudioEditStates.edit, F.data == "audio_cover")
async def edit_cover(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer(
        text="Отправь обложку трека", reply_markup=inline.menu
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

    print(state_data)

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
