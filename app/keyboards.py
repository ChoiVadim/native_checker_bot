from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Enter a message!",
    keyboard=[
        [
            KeyboardButton(text="English"),
            KeyboardButton(text="Korean"),
        ],
    ],
)
