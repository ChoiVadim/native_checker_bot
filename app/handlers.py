from enum import Enum

import asyncio
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.utils import kr_assistant, en_assistant
from app.keyboards import language_kb, en_inline_kb, kr_inline_kb
from app.helpers import check_request_limit
from app.config import Config

router = Router()


class Language(Enum):
    ENGLISH = "English"
    KOREAN = "Korean"


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = f"""Hi there👋
I`m here to help tidy up your messages to make them sound more natural and polished.
Just send one over, and I'll do my best to refine it for you! If you need translations, I can help with various languages too!

You can make up to {Config.REQUEST_LIMIT} requests within {int(Config.RESET_TIME.seconds // 60)} minutes.
    
Use /language to set your default language.
Use /buy to buy unlimited requests.
    
To get more requests, buy me a coffee 🤎☕
"""
    await message.answer_photo(
        photo=FSInputFile("app/assets/logo.jpg"),
        reply_markup=language_kb,
        caption=text,
    )


@router.message(Command("language"))
async def cmd_start(message: Message):
    msg = await message.answer("Click on the buttons below.", reply_markup=language_kb)
    await asyncio.sleep(10)
    await msg.delete()
    await message.delete()


@router.message(Command("buy"))
async def cmd_but(message: Message):
    caption = r"""💵 Unlock Unlimited Requests\! 💵

Gain access to unlimited requests by simply sending $10\. Once your payment is confirmed, I\'ll provide you with full, unrestricted access\.

📋 Payment Details\:
||Woori Bank\: 1002\-261\-902499||
||NongHyup Bank\:  356\-1428\-4014\-13||
||Hana Bank\:  149\-910332\-10507||

Feel free to reach out if you have any questions\. Thank you\!
"""
    await message.answer_photo(
        photo=FSInputFile("app/assets/buy.jpg"),
        caption=caption,
        parse_mode="MarkdownV2",
    )


@router.message(F.text == "English")
async def cmd_english(message: Message, state: FSMContext):
    await state.update_data({"language": Language.ENGLISH})
    msg = await message.answer("Default language was changed to English")
    await asyncio.sleep(3)
    await msg.delete()
    await message.delete()


@router.message(F.text == "Korean")
async def cmd_korean(message: Message, state: FSMContext):
    await state.update_data({"language": Language.KOREAN})
    msg = await message.answer("Default language was changed to Korean")
    await asyncio.sleep(3)
    await msg.delete()
    await message.delete()


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
    request_limit, wait_time = check_request_limit(message.from_user.id)

    if wait_time:
        await message.answer(f"Too many requests. Please wait {wait_time}.")
        return

    language = (await state.get_data()).get("language")

    assistant = en_assistant if language == Language.ENGLISH else kr_assistant
    kb = en_inline_kb if language == Language.ENGLISH else kr_inline_kb

    assistant.add_message_to_thread("user", message.text)

    await asyncio.to_thread(assistant.run_assistant)
    await asyncio.to_thread(assistant.wait_for_completion)
    await message.answer(assistant.get_response(), reply_markup=kb)


@router.callback_query(F.data == "get_audio")
async def get_audio(callback_query: CallbackQuery):
    request_limit, wait_time = check_request_limit(callback_query.from_user.id)

    if wait_time:
        await callback_query.answer(f"Too many requests. Please wait {wait_time}.")
        return

    await callback_query.answer("Getting audio...")
    await send_audio_message(
        callback_query.bot, callback_query.message.chat.id, callback_query.message.text
    )


@router.callback_query(F.data == "to_korean")
async def to_korean(callback_query: CallbackQuery):
    request_limit, wait_time = check_request_limit(callback_query.from_user.id)

    if wait_time:
        await callback_query.answer(f"Too many requests. Please wait {wait_time}.")
        return

    await callback_query.answer("Translating...")
    kr_assistant.add_message_to_thread("user", callback_query.message.text)
    await asyncio.to_thread(kr_assistant.run_assistant)
    await asyncio.to_thread(kr_assistant.wait_for_completion)
    await callback_query.message.edit_text(
        text=kr_assistant.get_response(), reply_markup=kr_inline_kb
    )


@router.callback_query(F.data == "to_english")
async def to_english(callback_query: CallbackQuery):
    request_limit, wait_time = check_request_limit(callback_query.from_user.id)

    if wait_time:
        await callback_query.answer(f"Too many requests. Please wait {wait_time}.")
        return

    await callback_query.answer("Translating...")
    en_assistant.add_message_to_thread("user", callback_query.message.text)
    await asyncio.to_thread(en_assistant.run_assistant)
    await asyncio.to_thread(en_assistant.wait_for_completion)
    await callback_query.message.edit_text(
        text=en_assistant.get_response(), reply_markup=en_inline_kb
    )
