import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID_STR = os.getenv("CHANNEL_ID")

if not BOT_TOKEN:
    raise RuntimeError("Не задана переменная окружения BOT_TOKEN")

if not CHANNEL_ID_STR:
    raise RuntimeError("Не задана переменная окружения CHANNEL_ID")

CHANNEL_ID = int(CHANNEL_ID_STR)

