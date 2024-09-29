from os import getenv
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    bot_token: str | None = getenv("BOT_TOKEN")
    admin_telegram_id: str | None = getenv("ADMIN_TELEGRAM_ID")
    en_assistant_id: str | None = getenv("EN_ASSISTANT_ID")
    kr_assistant_id: str | None = getenv("KR_ASSISTANT_ID")
    REDIS_URL: str | None = getenv("REDIS_URL")
    REDIS_PORT: str | None = getenv("REDIS_PORT")
    RESET_TIME: timedelta = timedelta(minutes=5)
    REQUEST_LIMIT: int = 5
