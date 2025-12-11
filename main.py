import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

from config import BOT_TOKEN, CHANNEL_ID

logging.basicConfig(level=logging.INFO)


async def start_handler(message: Message, bot: Bot):
    # Проверяем подписку на канал
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    except Exception as e:
        logging.exception("Ошибка при get_chat_member")
        await message.answer("Что-то пошло не так, попробуйте позже.")
        return

    if member.status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }:
        await message.answer("Подписка есть ✅")
    else:
        await message.answer("Похоже, вы не подписаны на канал.\n"
                             "Сначала подпишитесь, а потом снова нажмите /start")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")

    logging.info(f"Стартуем бота, CHANNEL_ID = {CHANNEL_ID}")

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, F.text == "/start")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
