import asyncio
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiogram.utils.markdown import hbold, hlink

from config import BOT_TOKEN
from parser import parse_clothes

cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_main_menu(bot):
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Запустить бота"),
            BotCommand(command="/about", description="Информация о боте"),
        ]
    )


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.reply("Готов приступить к работе")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужская одежда💁‍♂️")],
            [KeyboardButton(text="Женская одежда💁‍♀️")],
        ],
        resize_keyboard=True,
    )
    await message.answer("Выбери категорию: ", reply_markup=keyboard)


@dp.message(Command("about"))
async def about(message: Message):
    text = f"Привет! Я бот, который присылает актуальные списки одежды с сайта Ellesse для женщин и мужчин. Мой создатель - {hlink('sguschonka', 'https://github.com/sguschonka')}"
    await message.answer(text=text, parse_mode="HTML")


@dp.message(F.text == "Женская одежда💁‍♀️")
async def women_cloth(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="XS", callback_data="w_size_XS"),
                InlineKeyboardButton(text="S", callback_data="w_size_S"),
                InlineKeyboardButton(text="M", callback_data="w_size_M"),
                InlineKeyboardButton(text="L", callback_data="w_size_L"),
                InlineKeyboardButton(text="XL", callback_data="w_size_XL"),
                InlineKeyboardButton(text="14", callback_data="w_size_14"),
                InlineKeyboardButton(text="12", callback_data="w_size_12"),
            ],
            [
                InlineKeyboardButton(text="6", callback_data="w_size_6"),
                InlineKeyboardButton(text="8", callback_data="w_size_8"),
                InlineKeyboardButton(text="8.0", callback_data="w_size_8.0"),
                InlineKeyboardButton(text="14.0", callback_data="w_size_14.0"),
            ],
            [
                InlineKeyboardButton(text="6.0", callback_data="w_size_6.0"),
                InlineKeyboardButton(text="18", callback_data="w_size_18"),
                InlineKeyboardButton(text="20", callback_data="w_size_20"),
                InlineKeyboardButton(text="22", callback_data="w_size_22"),
            ],
            [
                InlineKeyboardButton(text="16.0", callback_data="w_size_16.0"),
                InlineKeyboardButton(text="10.0", callback_data="w_size_10.0"),
                InlineKeyboardButton(text="12.0", callback_data="w_size_12.0"),
            ],
        ]
    )

    await message.answer("Выберите размер", reply_markup=keyboard)


@dp.message(F.text == "Мужская одежда💁‍♂️")
async def men_cloth(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="XS", callback_data="m_size_XS"),
                InlineKeyboardButton(text="S", callback_data="m_size_S"),
                InlineKeyboardButton(text="M", callback_data="m_size_M"),
                InlineKeyboardButton(text="L", callback_data="m_size_L"),
                InlineKeyboardButton(text="XL", callback_data="m_size_XL"),
                InlineKeyboardButton(text="2XL", callback_data="m_size_2XL"),
                InlineKeyboardButton(text="3XL", callback_data="m_size_3XL"),
            ]
        ]
    )

    await message.answer("Выберите размер", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("m_size_"))
async def process_size_mens(callback: CallbackQuery):
    size = callback.data.replace("m_size_", "", 1)
    await callback.message.answer(
        f"Выбран размер: {size}. Пожалуйста подождите..."
    )
    gender = "mens"
    try:
        await parse_clothes(size, gender)

        with open(f"result_{cur_time}.json", encoding="utf-8") as f:
            data = json.load(f)

        cards_text = ""
        for item in data:
            card = (
                f"{hlink(item.get('title'), item.get('link'))}\n"
                f"{hbold('Цена: ')} {item.get('price')}💸\n"
                f"{hbold('Размер: ')} {item.get('size')}\n"
            )
            cards_text += card

            if len(cards_text) >= 3000:
                await callback.message.answer(cards_text, parse_mode="HTML", disable_web_page_preview=True)
                cards_text = ""
                await asyncio.sleep(1)
        if cards_text:
            await callback.message.answer(cards_text, parse_mode="HTML", disable_web_page_preview=True)

        await callback.message.answer(
            "Одежда успешно загружена, капитан! Хотите дать мне еще одну команду?"
        )
    except Exception as e:
        print(f"Ошибка!Error: {e}")
        await callback.message.answer("Произошла ошибка при обработке запроса")


@dp.callback_query(F.data.startswith("w_size_"))
async def process_size_womens(callback: CallbackQuery):
    size = callback.data.replace("w_size_", "", 1)
    await callback.message.answer(
        f"Выбран размер: {size}. Пожалуйста подождите..."
    )
    gender = "womens"
    try:
        await parse_clothes(size, gender)

        with open(f"result_{cur_time}.json", encoding="utf-8") as f:
            data = json.load(f)

        cards_text = ""
        for item in data:
            card = (
                f"{hlink(item.get('title'), item.get('link'))}\n"
                f"{hbold('Цена: ')} {item.get('price')}💸\n"
                f"{hbold('Размер: ')} {item.get('size')}\n"
            )
            cards_text += card

            if len(cards_text) >= 3000:
                await callback.message.answer(cards_text, parse_mode="HTML", disable_web_page_preview=True)
                cards_text = ""
                await asyncio.sleep(1)
        if cards_text:
            await callback.message.answer(cards_text, parse_mode="HTML", disable_web_page_preview=True)

        await callback.message.answer(
            "Одежда успешно загружена, капитан! Хотите дать мне еще одну команду?"
        )
    except Exception as e:
        print(f"Ошибка!Error: {e}")
        await callback.message.answer("Произошла ошибка при обработке запроса")


async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
