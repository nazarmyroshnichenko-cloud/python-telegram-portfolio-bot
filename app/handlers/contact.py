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

router = Router()

PROMPTS = {
    "en": ["What is your name?", "What is your email?", "Which service do you need?", "Please describe your project."],
    "uk": ["Як вас звати?", "Ваш email?", "Яка послуга вам потрібна?", "Опишіть, будь ласка, ваш проєкт."],
}


@router.message(Command("cancel"))
async def cancel_contact(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Request cancelled.", reply_markup=main_keyboard())


@router.message(F.text.in_({"Contact Me", "Зв'язатися"}))
async def begin_contact(message: Message, state: FSMContext) -> None:
    await state.set_state(ContactForm.name)
    await message.answer(PROMPTS["en"][0])


@router.message(ContactForm.name, F.text)
async def contact_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await state.set_state(ContactForm.email)
    await message.answer(PROMPTS["en"][1])


@router.message(ContactForm.email, F.text)
async def contact_email(message: Message, state: FSMContext) -> None:
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", message.text.strip()):
        await message.answer("Please enter a valid email address.")
        return
    await state.update_data(email=message.text.strip())
    await state.set_state(ContactForm.service)
    await message.answer(PROMPTS["en"][2])


@router.message(ContactForm.service, F.text)
async def contact_service(message: Message, state: FSMContext) -> None:
    await state.update_data(service=message.text.strip())
    await state.set_state(ContactForm.description)
    await message.answer(PROMPTS["en"][3])


@router.message(ContactForm.description, F.text)
async def contact_description(message: Message, state: FSMContext) -> None:
    data = await state.update_data(description=message.text.strip())
    async with SessionFactory() as session:
        request = ContactRequest(telegram_id=message.from_user.id, **data)
        session.add(request)
        await session.commit()
    settings = get_settings()
    await message.bot.send_message(settings.admin_id, f"New portfolio request from {data['name']} ({data['email']})\nService: {data['service']}\n\n{data['description']}")
    await state.clear()
    await message.answer("Thank you! Your request has been sent. I will get back to you soon.", reply_markup=main_keyboard())
