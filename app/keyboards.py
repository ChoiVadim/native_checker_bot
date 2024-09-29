from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

language_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Enter a message!",
    keyboard=[
        [
            KeyboardButton(text="English"),
            KeyboardButton(text="Korean"),
        ],
    ],
)

en_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔊", callback_data="get_audio"),
            InlineKeyboardButton(text="🇰🇷", callback_data="to_korean"),
        ],
    ],
)

kr_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔊", callback_data="get_audio"),
            InlineKeyboardButton(text="🇺🇸", callback_data="to_english"),
        ],
    ],
)
