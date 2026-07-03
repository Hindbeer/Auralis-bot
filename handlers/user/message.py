import os
from textwrap import dedent

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message, ReplyKeyboardRemove

from config import config
from keyboards import inline
from utils import AudioEditStates

router = Router()
bot = Bot(config.BOT_TOKEN)


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer_photo(
        photo="https://i.pinimg.com/1200x/21/7b/b5/217bb5ff1302e597371408a40b8c4a88.jpg",
        caption=dedent(f"""
        Добро пожаловать, <b>{message.from_user.first_name}</b>!
        
        Я могу поменять в твоем треке:
        <b>1)</b> обложку 🌅 
        <b>2)</b> название 📝 
        <b>3)</b> исполнителя 👤    
        
        Пришли мне свой трек в формате <code>.mp3</code> для этого"""),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AudioEditStates.audio)


@router.message(AudioEditStates.audio, F.audio)
async def get_track(message: Message, state: FSMContext):
    main_message_id = message.message_id
    audio_file = await bot.get_file(message.audio.file_id)
    await state.update_data(main_message_id=main_message_id, audio=audio_file)

    await message.answer_photo(
        photo="https://i.pinimg.com/736x/bf/6d/86/bf6d86326ba33ac1c1dc168e0f6591f1.jpg",
        caption=dedent(f"""
        <b>ℹ️ Информация о треке:</b>

        Исполнитель: <code>test</code>
        Название:  <code>{message.audio.title}</code>
        
        Название файла: <code>{message.audio.file_name}</code>
        """),
        reply_markup=inline.audio,
    )


@router.callback_query(AudioEditStates.audio, F.data == "audio_save")
async def save_track(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    audio_file = state_data["audio"]
    audio_filename = "audio-audio_file-auralis-bot.mp3"

    await bot.download_file(audio_file.file_path, audio_filename)

    reply_audio = FSInputFile(audio_filename, filename=audio_filename)
    await callback_query.message.answer_audio(audio=reply_audio)

    if os.path.exists(audio_filename):
        os.remove(audio_filename)

    await state.clear()
    await callback_query.answer()
