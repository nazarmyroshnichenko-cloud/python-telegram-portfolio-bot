from aiogram.fsm.state import State, StatesGroup


class ContactForm(StatesGroup):
    name = State()
    email = State()
    service = State()
    description = State()
