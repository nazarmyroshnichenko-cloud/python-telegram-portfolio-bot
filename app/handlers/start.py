from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.database.db import SessionFactory
from app.database.models import User
from app.keyboards.main import language_keyboard, main_keyboard

router = Router()

TEXT = {
    "en": {
        "welcome": "Hello! I’m Nazar, a Python Telegram Bot Developer.\n\nI build reliable bots, automation tools, API integrations and database-driven solutions.",
        "language": "Choose your language:",
        "changed": "Language updated.",
    },
    "uk": {
        "welcome": "Вітаю! Я Назар, Python-розробник Telegram-ботів.\n\nЯ створюю надійних ботів, інструменти автоматизації, API-інтеграції та рішення з базами даних.",
        "language": "Оберіть мову:",
        "changed": "Мову оновлено.",
    },
}


async def get_language(user_id: int) -> str:
    async with SessionFactory() as session:
        user = await session.get(User, user_id)
        return user.language if user and user.language else "en"


async def save_user(message: Message, language: str | None = None) -> None:
    language = language or message.from_user.language_code or "en"
    if language not in TEXT:
        language = "en"
    async with SessionFactory() as session:
        user = await session.get(User, message.from_user.id)
        if user is None:
            session.add(User(id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name, language=language))
        else:
            user.username = message.from_user.username
            user.full_name = message.from_user.full_name
        await session.commit()



@router.message(CommandStart())
async def start(message: Message) -> None:
    await save_user(message)
    language = await get_language(message.from_user.id)
    await message.answer(TEXT[language]["welcome"], reply_markup=main_keyboard(language))


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    language = await get_language(message.from_user.id)
    await message.answer("Use the menu below to explore my portfolio or send a project request.", reply_markup=main_keyboard(language))


@router.message(lambda message: message.text in {"Language", "Мова"})
async def choose_language(message: Message) -> None:
    await message.answer("Choose your language / Оберіть мову:", reply_markup=language_keyboard())


@router.callback_query(lambda callback: callback.data and callback.data.startswith("lang:"))
async def set_language(callback: CallbackQuery) -> None:
    language = callback.data.split(":", 1)[1]
    async with SessionFactory() as session:
        user = await session.get(User, callback.from_user.id)
        if user:
            user.language = language
            await session.commit()
    await callback.message.answer(TEXT[language]["changed"], reply_markup=main_keyboard(language))
    await callback.answer()
