from decouple import config

ADMIN_ID = config("ADMIN_ID", default="")
BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", cast=int, default=8000)
WEBHOOK_PATH = config("WEBHOOK_PATH", default="webhook")
BASE_URL = config("BASE_URL")
GAME_DB_PATH = config("GAME_DB_PATH", default="game.db")
