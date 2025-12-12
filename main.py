import asyncio
import logging
import os
import socket
import time

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, CHANNEL_ID

logging.basicConfig(level=logging.INFO)

INSTANCE = f"host={socket.gethostname()} pid={os.getpid()} t={int(time.time())}"


async def start_handler(message: Message, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    except Exception:
        logging.exception(f"[{INSTANCE}] Ошибка при get_chat_member")
        await message.answer("Что-то пошло не так 😵 Попробуйте позже.")
        return

    if member.status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,  # <-- ВОТ ЭТО ВАЖНО
    }:
        await message.answer("Подписка есть ✅")
    else:
        await message.answer(
            "Похоже, вы не подписаны на канал.\n"
            "Сначала подпишитесь, а потом снова нажмите /start"
        )


async def fallback_handler(message: Message):
    logging.info(f"[{INSTANCE}] Unhandled message: {message.text!r}")
    await message.answer("Я тебя вижу 🙂 Напиши /start, чтобы проверить подписку.")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")

    logging.info(f"[{INSTANCE}] Стартуем бота, CHANNEL_ID = {CHANNEL_ID}")

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(fallback_handler, F.text)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
