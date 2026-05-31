import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен, полученный у @BotFather
API_TOKEN = '8224621644:AAEpIxYGIvQNOzd-KncEd253V9ovzh9mvsI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Имитация базы данных товаров
PRODUCTS = {
    "1": {"name": "Цифровой курс по Python", "price": 990, "desc": "Полное руководство для новичков."},
    "2": {"name": "Гайд по заработку", "price": 450, "desc": "10 проверенных способов в 2024 году."},
}

# Главное меню
def main_menu():
    buttons = [
        [InlineKeyboardButton(text="🛍 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Стартовая команда
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Добро пожаловать в наш магазин!", reply_markup=main_menu())

# Обработка каталога
@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    keyboard = []
    for product_id, info in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(text=f"{info['name']} - {info['price']} руб.", callback_data=f"product_{product_id}")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")])
    
    await callback.message.edit_text("Выберите интересующий товар:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

# Карточка товара
@dp.callback_query(F.data.startswith("product_"))
async def show_product(callback: types.CallbackQuery):
    product_id = callback.data.split("_")[1]
    product = PRODUCTS[product_id]
    
    text = f"📦 *{product['name']}*\n\n{product['desc']}\n\n💰 Цена: {product['price']} руб."
    keyboard = [
        [InlineKeyboardButton(text="💳 Купить", callback_data=f"buy_{product_id}")],
        [InlineKeyboardButton(text="⬅️ К каталогу", callback_data="catalog")]
    ]
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())