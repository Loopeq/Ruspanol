from aiogram.filters.callback_data import CallbackData


class QuizCallbackData(CallbackData, prefix="quiz"):
    section_id: int
    stage: int

