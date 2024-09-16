from enum import Enum

import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.keyboards import main_kb as kb
from app.utils import kr_assistant, en_assistant


router = Router()


class Language(Enum):
    ENGLISH = "English"
    KOREAN = "Korean"


language = Language.ENGLISH


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Hi, I`m here to check your messages and make it better!", reply_markup=kb
    )


@router.message(F.text == "English")
async def cmd_english(message: Message):
    global language
    language = Language.ENGLISH
    await message.answer("Changing language to English")


@router.message(F.text == "Korean")
async def cmd_korean(message: Message):
    global language
    language = Language.KOREAN
    await message.answer("Changing language to Korean")


@router.message()
async def send_message(message: Message):
    if language == Language.ENGLISH:
        en_assistant.add_message_to_thread("user", message.text)
        await asyncio.to_thread(en_assistant.run_assistant)
        await asyncio.to_thread(en_assistant.wait_for_completion)
        await message.answer(en_assistant.get_response())
    elif language == Language.KOREAN:
        kr_assistant.add_message_to_thread("user", message.text)
        await asyncio.to_thread(kr_assistant.run_assistant)
        await asyncio.to_thread(kr_assistant.wait_for_completion)
        await message.answer(kr_assistant.get_response())
