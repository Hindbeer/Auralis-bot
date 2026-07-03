from textwrap import dedent

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer_photo(
        photo="https://i.pinimg.com/1200x/21/7b/b5/217bb5ff1302e597371408a40b8c4a88.jpg",
        caption=dedent(f"""
        Добро пожаловать, <b>{message.from_user.first_name}</b>!
        
        Я могу поменять в твоем треке:
        <b>1)</b> обложку 🌅 
        <b>2)</b> название 📑 
        <b>3)</b> артиста 👨‍👧‍👧    
        
        Пришли мне свой трек в формате <code>.mp3</code> для этого"""),
    )
