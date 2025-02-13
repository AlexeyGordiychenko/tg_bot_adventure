from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config


ADMIN_ID = config("ADMIN_ID")
BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = int(config("PORT"))
WEBHOOK_PATH = f"/{BOT_TOKEN}"
BASE_URL = config("BASE_URL")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
