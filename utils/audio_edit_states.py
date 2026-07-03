from aiogram.fsm.state import State, StatesGroup


class AudioEditStates(StatesGroup):
    audio = State()
    cover = State()
    title = State()
    artist = State()
    save = State()
