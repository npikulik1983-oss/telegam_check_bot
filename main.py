import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)

        if member.status in ["member", "administrator", "creator"]:
            await message.answer("Ты подписан. Добро пожаловать!")
        else:
            await message.answer("Ты пока не подписан на канал. Подпишись, пожалуйста.")
    except Exception:
        await message.answer(
            "Не могу проверить подписку. Добавь бота в канал администратором."
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
