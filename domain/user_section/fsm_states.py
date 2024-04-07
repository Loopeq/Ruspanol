from aiogram.fsm.state import StatesGroup, State


class UserSectionQuizState(StatesGroup):
    add_answer = State()