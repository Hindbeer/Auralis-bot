import os

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_i18n import I18nContext

# from mutagen.id3 import APIC, ID3, TIT2, TPE1
from config import config
from keyboards import inline
from utils import AudioEditer, AudioEditStates, LanguageCallback, converte_to_mp3

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
async def save_track(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18nContext
) -> None:
    wait_message = await callback_query.message.answer("⏳")

    state_data = await state.get_data()

    try:
        converte_to_mp3(state_data["audio_filename"])

        audio_editer = AudioEditer(state_data["audio_filename"])
        audio_editer.edit_artist(state_data["audio_artist"])
        audio_editer.edit_title(state_data["audio_title"])
        audio_editer.edit_cover(state_data["cover_filename"])
        audio_editer.save_file()

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
    except Exception:
        await callback_query.message.answer(i18n.get())
    finally:
        await wait_message.delete()

    if os.path.exists(state_data["audio_filename"]):
        os.remove(state_data["audio_filename"])
    if state_data["cover_filename"] != "none-cover.jpg":
        os.remove(state_data["cover_filename"])

    await state.set_state(AudioEditStates.audio)
    await callback_query.answer()
