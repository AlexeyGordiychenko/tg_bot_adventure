from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config


ADMIN_ID = config("ADMIN_ID", default="")
BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST", default="0.0.0.0")
PORT = int(config("PORT", default=8000))
WEBHOOK_PATH = f"/webhook"
BASE_URL = config("BASE_URL")
GAME_DB_PATH = config("GAME_DB_PATH", default="game.db")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
