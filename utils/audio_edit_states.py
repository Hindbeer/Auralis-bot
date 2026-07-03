from aiogram.fsm.state import State, StatesGroup


class AudioEditStates(StatesGroup):
    audio = State()
    cover = State()
    media_tags = State()
    save = State()
