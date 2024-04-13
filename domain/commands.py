from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries import insert_user, get_sections
from domain.sections import get_sections_ikb, SectionsState

from domain.user_section.us_keyboards.keyboards import inline_user_sections_kb
from resources.strings import Strings


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(Strings.entry_info)
    try:
        insert_user(str(message.from_user.id))
    except Exception:
        return


@router.message(Command('sections'))
async def cmd_sections(message: Message, state: FSMContext):
    sections = get_sections()
    await message.answer(Strings.sections_info,
                         reply_markup=get_sections_ikb(sections=sections))
    await state.set_state(SectionsState.change_page)


@router.message(Command('profile'))
async def cmd_profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Профиль")


@router.message(Command('my_sections'))
async def cmd_user_sections(message: Message):
    await message.answer(Strings.available_user_sections, reply_markup=inline_user_sections_kb(message.from_user.id))
