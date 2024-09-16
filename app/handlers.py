from enum import Enum

import asyncio
from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
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
    await message.answer("Changing language to English", reply_markup=kb)


@router.message(F.text == "Korean")
async def cmd_korean(message: Message):
    global language
    language = Language.KOREAN
    await message.answer("Changing language to Korean", reply_markup=kb)


async def send_audio_message(bot: Bot | None, chat_id: int, text: str):
    # Get the audio stream from text_to_speech
    en_assistant.text_to_speech(text)
    if bot is None:
        return

    await bot.send_voice(
        chat_id=chat_id,
        voice=FSInputFile("speech.mp3"),
    )


@router.message()
async def send_message(message: Message):
    if language == Language.ENGLISH:
        en_assistant.add_message_to_thread("user", message.text)
        await asyncio.to_thread(en_assistant.run_assistant)
        await asyncio.to_thread(en_assistant.wait_for_completion)
        await message.answer(en_assistant.get_response(), reply_markup=kb)
        # Generate and send the audio message
        await send_audio_message(
            message.bot, message.chat.id, en_assistant.get_response()
        )
    elif language == Language.KOREAN:
        kr_assistant.add_message_to_thread("user", message.text)
        await asyncio.to_thread(kr_assistant.run_assistant)
        await asyncio.to_thread(kr_assistant.wait_for_completion)
        await message.answer(kr_assistant.get_response(), reply_markup=kb)
        await send_audio_message(
            message.bot, message.chat.id, kr_assistant.get_response()
        )
