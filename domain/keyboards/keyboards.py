import aiogram.utils.keyboard
import aiogram
from aiogram import types


from domain.filters.filters import  QuizCallbackData
from resources.strings import Strings


def inline_section_kb(data: list[dict]):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    buttons = [types.InlineKeyboardButton(text=obj["title"], callback_data=f"section{str(obj['id'])}" ) for obj in data]
    for button in buttons:
        builder.row(button, width=1)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)



def inline_words_kb(words):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for word in words:
        builder.add(types.InlineKeyboardButton(text=f"{word['espanol']}", callback_data=f'word{word["id"]}'))
        builder.add(types.InlineKeyboardButton(text=f"{word['russian']}", callback_data=f'word{word["id"]}'))
    builder.adjust(4)
    builder.row(types.InlineKeyboardButton(text=Strings.start_quiz,
                                           callback_data=QuizCallbackData(stage=0, section_id=words[0]["section_id"]).pack()), width=1)
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_return_to_words(section_id: int):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.quit_button, callback_data=f"return_to_words{section_id}"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_return_to_section_kb():
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_delete_voice(word_id):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.delete_voice_button, callback_data=f"delete_voice{word_id}"), width=1)
    return builder.as_markup(resize_keyboard=True)