import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os
import asyncio

API_TOKEN = os.getenv("7669433341:AAFa0MIXvWx2SbS_oC8eWY8aNFI8uombAVI")
CHANNEL_ID = os.getenv("-1002872296874")  # Пример: -1001234567890

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)

    if chat_member.status in ['member', 'creator', 'administrator']:
        await message.answer("Добро пожаловать! Вы успешно подписались и можете пользоваться ботом.")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("🔔 Подписаться на канал", url=f"https://t.me/{os.getenv('CHANNEL_USERNAME')}"),
            InlineKeyboardButton("✅ Проверить подписку", callback_data="check_sub")
        )
        await message.answer("❗️ Чтобы пользоваться ботом, необходимо подписаться на канал.", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)

    if chat_member.status in ['member', 'creator', 'administrator']:
        await bot.answer_callback_query(callback_query.id, "✅ Подписка подтверждена!")
        await bot.send_message(user_id, "Теперь вы можете пользоваться ботом.")
    else:
        await bot.answer_callback_query(callback_query.id, "❗️ Вы ещё не подписались на канал.", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
