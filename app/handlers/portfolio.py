from aiogram import F, Router
from aiogram.types import Message

from app.keyboards.main import links_keyboard

router = Router()

MESSAGES = {
    "About Me": "<b>About Me</b>\n\nI build Telegram bots and automation tools with Python, focusing on clean architecture, async workflows, API integrations and practical business value.",
    "Про мене": "<b>Про мене</b>\n\nЯ створюю Telegram-ботів та інструменти автоматизації на Python, приділяючи увагу чистій архітектурі, асинхронності, API-інтеграціям і користі для бізнесу.",
    "Skills": "<b>Skills</b>\n\n• Python\n• aiogram 3 and asyncio\n• FSM and routers\n• PostgreSQL and SQLite\n• REST APIs and aiohttp\n• Docker, Git and GitHub",
    "Навички": "<b>Навички</b>\n\n• Python\n• aiogram 3 та asyncio\n• FSM і routers\n• PostgreSQL та SQLite\n• REST API та aiohttp\n• Docker, Git і GitHub",
    "Services": "<b>Services</b>\n\n• Telegram bot development\n• Custom chatbot development\n• API and database integration\n• Automation\n• Bug fixing and maintenance\n• Deployment",
    "Послуги": "<b>Послуги</b>\n\n• Розробка Telegram-ботів\n• Індивідуальні чат-боти\n• Інтеграція API та баз даних\n• Автоматизація\n• Виправлення помилок і підтримка\n• Деплой",
    "Projects": "<b>Projects</b>\n\n<b>Portfolio Bot</b> — an English/Ukrainian portfolio with FSM contact forms and PostgreSQL.\n\n<b>API Product Bot</b> — asynchronous REST API integration using aiohttp.\n\n<b>Registration Bot</b> — multi-step FSM validation.\n\n<b>User Management Bot</b> — database operations and user records.",
    "Проєкти": "<b>Проєкти</b>\n\n<b>Portfolio Bot</b> — портфоліо англійською та українською з FSM-формою і PostgreSQL.\n\n<b>API Product Bot</b> — асинхронна REST API-інтеграція через aiohttp.\n\n<b>Registration Bot</b> — покрокова FSM-валидація.\n\n<b>User Management Bot</b> — робота з базою даних.",
}


@router.message(F.text.in_(MESSAGES.keys()))
async def show_portfolio_section(message: Message) -> None:
    await message.answer(MESSAGES[message.text], parse_mode="HTML", reply_markup=links_keyboard() if message.text in {"About Me", "Про мене"} else None)
