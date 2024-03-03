import aiogram.utils.keyboard
from aiogram import types
from strings import Strings


def main_kb():
    kb = [[types.KeyboardButton(text="Разделы")]]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def inline_section_kb(data: list[dict]):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    buttons = [types.InlineKeyboardButton(text=obj["title"], callback_data="section" + str(obj["id"])) for obj in data]
    for button in buttons:
        builder.row(button, width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_subsection_kb(data: list[dict]):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    buttons = [types.InlineKeyboardButton(text=obj["title"], callback_data="subsection" + str(obj["id"])) for obj in data]
    for button in buttons:
        builder.row(button, width=1)
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_return_to_section_kb():
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_return_to_subsection_kb(section_id):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data=f"section{section_id}"), width=1)
    return builder.as_markup(resize_keyboard=True)


def inline_words_kb(section_id, words):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for word in words:
        builder.add(types.InlineKeyboardButton(text=f"{word['espanol']}", callback_data="0"))
        builder.add(types.InlineKeyboardButton(text=f"{word['russian']}", callback_data="0"))
    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data=f"section{section_id}"), width=1)
    return builder.as_markup(resize_keyboard=True)
