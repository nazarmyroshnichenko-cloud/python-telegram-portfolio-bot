# Nazar's Portfolio Telegram Bot

An English/Ukrainian Telegram portfolio bot built with Python and aiogram 3.

## Features

- Bilingual portfolio interface: English and Ukrainian
- About, skills, services and projects sections
- FSM-based contact request form
- Email validation
- PostgreSQL persistence through SQLAlchemy async
- Admin notifications for new requests
- Docker and Railway-ready deployment

## Local setup

1. Create a bot with BotFather and copy `.env.example` to `.env`.
2. Fill in `BOT_TOKEN`, `ADMIN_ID`, and `DATABASE_URL`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start PostgreSQL with `docker compose up -d postgres`.
5. Run the bot: `python main.py`.

Never commit `.env` or expose a bot token publicly. If a token has been shared, revoke it in BotFather and generate a new one.

## Railway deployment

Create a Railway project with a PostgreSQL service and deploy this repository as a service. Add the environment variables from `.env.example`, setting `DATABASE_URL` to Railway's PostgreSQL connection string. The service starts with `python main.py`.

## Tech stack

Python, aiogram 3, asyncio, FSM, SQLAlchemy, PostgreSQL, aiohttp-ready architecture, Docker, Git and GitHub.
