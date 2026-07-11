import os
from textwrap import dedent

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext

from config import config
from keyboards import inline
from utils import AudioEditStates

router = Router()
bot = Bot(config.BOT_TOKEN)


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    print(
        f"DEBUG: User language={message.from_user.language_code}, I18n locale={i18n.locale}"
    )
    await state.clear()
    # await message.answer_photo(
    #     photo=FSInputFile("cat.jpg"),
    #     caption=dedent(f"""
    #     Добро пожаловать, <b>{message.from_user.first_name}</b>!

    #     Я могу поменять в твоем треке:
    #     <b>1)</b> обложку 🌅
    #     <b>2)</b> название 📝
    #     <b>3)</b> исполнителя 👤

    #     Пришли мне свой трек в формате <code>.mp3</code> для этого"""),
    #     reply_markup=ReplyKeyboardRemove(),
    # )

    await message.answer_photo(
        photo=FSInputFile("cat.jpg"),
        caption=i18n.get("welcome", name=message.from_user.first_name),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AudioEditStates.audio)


@router.message(Command("ru"))
async def set_ru_lang(message: Message, i18n: I18nContext) -> None:
    await i18n.set_locale("ru")
    await message.answer("ru")


@router.message(Command("en"))
async def set_en_lang(message: Message, i18n: I18nContext) -> None:
    await i18n.set_locale("en")
    await message.answer("en")


def get_captions(artist: str, title: str, filename: str) -> str:
    return dedent(f"""
    <b>ℹ️ Информация о треке:</b>

    Исполнитель: <code>{artist}</code>
    Название:  <code>{title}</code>
        
    Название файла: <code>{filename}</code>""")


async def send_edit_message(message: Message, caption: str, cover: FSInputFile) -> None:
    await message.answer_photo(
        photo=cover,
        caption=caption,
        reply_markup=inline.audio,
    )


# @router.message(AudioEditStates.audio, F.audio)
@router.message(F.audio)
async def get_track(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    # try:
    #     if os.path.exists(state_data["audio_filename"]):
    #         os.remove(state_data["audio_filename"])
    #     if state_data["cover_filename"] != "none-cover.jpg":
    #         os.remove(state_data["cover_filename"])
    # except TypeError as e:
    #     print(f"A type error occurred: {e}")

    audio_file = await bot.get_file(message.audio.file_id)
    audio_filename = f"{audio_file.file_id}-auralis-bot.mp3"
    await bot.download_file(audio_file.file_path, audio_filename)

    if message.audio.thumbnail:
        cover_file = await bot.get_file(message.audio.thumbnail.file_id)
        cover_filename = f"{cover_file.file_id}-auralis-bot.jpg"
        await bot.download_file(cover_file.file_path, cover_filename)
    else:
        cover_filename = "none-cover.jpg"

    await state.update_data(
        audio_filename=audio_filename,
        audio_artist=message.audio.performer,
        audio_title=message.audio.title,
        cover_filename=cover_filename,
    )

    cover = FSInputFile(state_data["cover_filename"])
    caption = get_captions(
        state_data["audio_artist"],
        state_data["audio_title"],
        state_data["audio_filename"],
    )
    await message.answer_photo(
        photo=cover,
        caption=caption,
        reply_markup=inline.audio,
    )

    await state.set_state(AudioEditStates.edit)


@router.message(AudioEditStates.title, F.text)
async def edit_title(message: Message, state: FSMContext) -> None:
    audio_title = message.text
    await state.update_data(audio_title=audio_title)

    state_data = await state.get_data()
    cover = FSInputFile(state_data["cover_filename"])
    caption = get_captions(
        state_data["audio_artist"],
        state_data["audio_title"],
        state_data["audio_filename"],
    )
    await message.answer_photo(
        photo=cover,
        caption=caption,
        reply_markup=inline.audio,
    )

    await state.set_state(AudioEditStates.edit)


@router.message(AudioEditStates.artist, F.text)
async def edit_artist(message: Message, state: FSMContext) -> None:
    audio_artist = message.text
    await state.update_data(audio_artist=audio_artist)

    state_data = await state.get_data()
    cover = FSInputFile(state_data["cover_filename"])
    caption = get_captions(
        state_data["audio_artist"],
        state_data["audio_title"],
        state_data["audio_filename"],
    )
    await message.answer_photo(
        photo=cover,
        caption=caption,
        reply_markup=inline.audio,
    )

    await state.set_state(AudioEditStates.edit)


@router.message(AudioEditStates.cover, F.photo)
async def edit_cover(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    cover_file = await bot.get_file(message.photo[2].file_id)
    print(message.photo)
    cover_filename = (
        f"{cover_file.file_id}-auralis-bot.jpg"
        if state_data["cover_filename"] == "none-cover.jpg"
        else state_data["cover_filename"]
    )
    await state.update_data(cover_filename=cover_filename)
    await bot.download_file(cover_file.file_path, cover_filename)

    state_data = await state.get_data()
    cover = FSInputFile(state_data["cover_filename"])
    caption = get_captions(
        state_data["audio_artist"],
        state_data["audio_title"],
        state_data["audio_filename"],
    )
    await message.answer_photo(
        photo=cover,
        caption=caption,
        reply_markup=inline.audio,
    )

    await state.set_state(AudioEditStates.edit)
