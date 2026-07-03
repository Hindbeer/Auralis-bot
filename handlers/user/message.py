from textwrap import dedent

from utils import AudioEditStates
from keyboards import inline

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


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
    audio_filename = f"audio-{message.from_user.id}-auralis-bot.mp3"

    await message.answer_photo(
        photo="https://i.pinimg.com/736x/bf/6d/86/bf6d86326ba33ac1c1dc168e0f6591f1.jpg",
        caption=dedent(f"""
        <b>ℹ️ Информация о треке:</b>

        Исполнитель: <code>test</code>
        Название:  <code>тест</code>
        
        Название файла: <code>{audio_filename}</code>
        """),
        reply_markup=inline.audio,
    )
