import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, CHANNEL_ID

logging.basicConfig(level=logging.INFO)


async def start_handler(message: Message, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    except Exception:
        logging.exception("Ошибка при get_chat_member")
        await message.answer("Что-то пошло не так 😵 Попробуйте позже.")
        return

    if member.status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }:
        await message.answer("Подписка есть ✅")
    else:
        await message.answer(
            "Похоже, вы не подписаны на канал.\n"
            "Сначала подпишитесь, а потом снова нажмите /start"
        )


async def fallback_handler(message: Message):
    logging.info(f"Unhandled message: {message.text!r}")
    await message.answer("Я тебя вижу 🙂 Напиши /start, чтобы проверить подписку.")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")

    logging.info(f"Стартуем бота, CHANNEL_ID = {CHANNEL_ID}")

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    # Хэндлер на /start
    dp.message.register(start_handler, CommandStart())

    # Запасной хэндлер на любой текст
    dp.message.register(fallback_handler, F.text)

    # ВАЖНО: если где-то был webhook, он будет мешать polling и вызывать конфликт
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

