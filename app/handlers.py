from enum import Enum

import asyncio
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.utils import kr_assistant, en_assistant
from app.keyboards import main_kb, inline_kb

router = Router()


class Language(Enum):
    ENGLISH = "English"
    KOREAN = "Korean"


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Hi, I'm here to review your messages and make them sound more natural and polished! Just send me one, and I'll do my best!",
        reply_markup=main_kb,
    )


@router.message(F.text == "English")
async def cmd_english(message: Message, state: FSMContext):
    await state.update_data({"language": Language.ENGLISH})
    await message.answer("Changing language to English", reply_markup=main_kb)


@router.message(F.text == "Korean")
async def cmd_korean(message: Message, state: FSMContext):
    await state.update_data({"language": Language.KOREAN})
    await message.answer("Changing language to Korean", reply_markup=main_kb)


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
async def send_message(message: Message, state: FSMContext):
    language = (await state.get_data()).get("language")

    assistant = en_assistant if language == Language.ENGLISH else kr_assistant
    assistant.add_message_to_thread("user", message.text)

    await asyncio.to_thread(assistant.run_assistant)
    await asyncio.to_thread(assistant.wait_for_completion)
    await message.answer(assistant.get_response(), reply_markup=inline_kb)


@router.callback_query(F.data == "get_audio")
async def get_audio(callback_query: CallbackQuery):
    await callback_query.answer("Getting audio...")
    await send_audio_message(
        callback_query.bot, callback_query.message.chat.id, callback_query.message.text
    )
