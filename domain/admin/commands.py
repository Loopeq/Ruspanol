import enum

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from data.queries.phrases import insert_phrase, select_current_phrase
from domain.admin.callback_models import AdminMenuCallbackData, BasicAdminActions, CheckActions
from domain.admin.keyboards import admin_menu_ikb, admin_check_ikb
from domain.filters import IsAdminFilter
from domain.shemas.schemas_dto import PhrasesAddDto


class AdminCommands(enum.StrEnum):
    admin = "admin"


class AddPhraseState(StatesGroup):
    add_ru = State()
    add_es = State()


router = Router()


@router.message(Command(AdminCommands.admin), IsAdminFilter())
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Admin Menu", reply_markup=admin_menu_ikb())


@router.callback_query(AdminMenuCallbackData.filter(F.action == BasicAdminActions.add_phrase))
async def admin_add_phrase(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("(ADD PHRASE) Enter espanol phrase: ")
    await state.set_state(AddPhraseState.add_es)
    await callback.answer()


@router.message(StateFilter(AddPhraseState.add_es))
async def add_es_phrase(message: Message, state: FSMContext):
    await message.answer(f"(ADD PHRASE) Espanol phrase:\n{message.text}", reply_markup=admin_check_ikb())
    await state.update_data(data={"es": message.text})


@router.message(StateFilter(AddPhraseState.add_ru))
async def add_ru_phrase(message: Message, state: FSMContext):
    await message.answer(f"(ADD PHRASE) Russian translate:\n{message.text}", reply_markup=admin_check_ikb())
    await state.update_data(data={"ru": message.text})


@router.callback_query(StateFilter(AddPhraseState.add_es),
                       AdminMenuCallbackData.filter(F.action.in_({CheckActions.check_no, CheckActions.check_yes})))
async def check_es_phrase(callback: CallbackQuery, callback_data: AdminMenuCallbackData, state: FSMContext):
    if callback_data.action == CheckActions.check_yes:
        await callback.message.edit_text(text="(ADD PHRASE) Enter russian translate:")
        await state.set_state(AddPhraseState.add_ru)
    elif callback_data.action == CheckActions.check_no:
        await callback.message.edit_text(text="(ADD PHRASE) Enter espanol phrase: ")
    await callback.answer()


@router.callback_query(StateFilter(AddPhraseState.add_ru),
                       AdminMenuCallbackData.filter(F.action.in_({CheckActions.check_no, CheckActions.check_yes})))
async def check_ru_phrase(callback: CallbackQuery, callback_data: AdminMenuCallbackData, state: FSMContext):
    data = await state.get_data()
    ru_word, es_word = data["ru"], data["es"]
    if callback_data.action == CheckActions.check_yes:
        await state.clear()
        await callback.message.edit_text(text=f"Inserted:\n {es_word}\n {ru_word}")
        await insert_phrase(phrase=PhrasesAddDto(ru=ru_word, es=es_word))
    elif callback_data.action == CheckActions.check_no:
        await callback.message.edit_text(text="(ADD PHASE) Enter russian translate")
    await callback.answer()


@router.callback_query(StateFilter(AddPhraseState),
                       AdminMenuCallbackData.filter(F.action == BasicAdminActions.cancel_add_phrase))
async def cancel_add_phrase(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
