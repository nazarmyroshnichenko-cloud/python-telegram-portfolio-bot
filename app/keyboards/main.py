from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def main_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    labels = {
        "en": ["About Me", "Skills", "Projects", "Services", "Contact Me", "Language"],
        "uk": ["Про мене", "Навички", "Проєкти", "Послуги", "Зв'язатися", "Мова"],
    }
    about, skills, projects, services, contact, language_label = labels.get(language, labels["en"])
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=about), KeyboardButton(text=skills)],
            [KeyboardButton(text=projects), KeyboardButton(text=services)],
            [KeyboardButton(text=contact), KeyboardButton(text=language_label)],
        ],
        resize_keyboard=True,
    )


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="English", callback_data="lang:en"),
        InlineKeyboardButton(text="Українська", callback_data="lang:uk"),
    ]])


def links_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="GitHub", url="https://github.com/nazarmyroshnichenko-cloud"),
        InlineKeyboardButton(text="Telegram", url="https://t.me/i_amnazi66"),
    ]])
