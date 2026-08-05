import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import get_settings
from app.database.db import SessionFactory
from app.database.models import ContactRequest
from app.keyboards.main import main_keyboard
from app.states.contact import ContactForm
from app.handlers.start import get_language

router = Router()

PROMPTS = {
    "en": ["What is your name?", "What is your email?", "Which service do you need?", "Please describe your project."],
    "uk": ["Як вас звати?", "Ваш email?", "Яка послуга вам потрібна?", "Опишіть, будь ласка, ваш проєкт."],
}

CANCEL_TEXT = {
    "en": "Request cancelled.",
    "uk": "Запит скасовано.",
}

SUCCESS_TEXT = {
    "en": "Thank you! Your request has been sent. I will get back to you soon.",
    "uk": "Дякую! Ваш запит надіслано. Я зв'яжуся з вами найближчим часом.",
}

INVALID_EMAIL_TEXT = {
    "en": "Please enter a valid email address.",
    "uk": "Будь ласка, введіть коректну email-адресу.",
}


@router.message(Command("cancel"))
async def cancel_contact(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = data.get("language", "en")
    await state.clear()
    await message.answer(CANCEL_TEXT[language], reply_markup=main_keyboard(language))


@router.message(F.text.in_({"Contact Me", "Зв'язатися"}))
async def begin_contact(message: Message, state: FSMContext) -> None:
    language = await get_language(message.from_user.id)
    await state.update_data(language=language)
    await state.set_state(ContactForm.name)
    await message.answer(PROMPTS[language][0], reply_markup=main_keyboard(language))


@router.message(ContactForm.name, F.text)
async def contact_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    data = await state.get_data()
    language = data.get("language", "en")
    await state.set_state(ContactForm.email)
    await message.answer(PROMPTS[language][1], reply_markup=main_keyboard(language))


@router.message(ContactForm.email, F.text)
async def contact_email(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = data.get("language", "en")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", message.text.strip()):
        await message.answer(INVALID_EMAIL_TEXT[language], reply_markup=main_keyboard(language))
        return

    await state.update_data(email=message.text.strip())
    await state.set_state(ContactForm.service)
    await message.answer(PROMPTS[language][2], reply_markup=main_keyboard(language))


@router.message(ContactForm.service, F.text)
async def contact_service(message: Message, state: FSMContext) -> None:
    await state.update_data(service=message.text.strip())
    data = await state.get_data()
    language = data.get("language", "en")
    await state.set_state(ContactForm.description)
    await message.answer(PROMPTS[language][3], reply_markup=main_keyboard(language))


@router.message(ContactForm.description, F.text)
async def contact_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text.strip())
    data = await state.get_data()
    language = data.get("language", "en")

    # Сохраняем в БД (явно передаём поля, без language)
    async with SessionFactory() as session:
        request = ContactRequest(
            telegram_id=message.from_user.id,
            name=data["name"],
            email=data["email"],
            service=data["service"],
            description=data["description"],
        )
        session.add(request)
        await session.commit()

    # Уведомляем админа
    settings = get_settings()
    await message.bot.send_message(
        settings.admin_id,
        f"New portfolio request from {data['name']} ({data['email']})\n"
        f"Service: {data['service']}\n\n{data['description']}"
    )

    await state.clear()
    await message.answer(SUCCESS_TEXT[language], reply_markup=main_keyboard(language))