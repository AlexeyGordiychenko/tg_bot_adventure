from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from aiogram import types
import uvicorn
from create_bot import bot, dp, BASE_URL, WEBHOOK_PATH, HOST, PORT, ADMIN_ID
from handlers import router
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands():
    commands = [BotCommand(command="start", description="Start the game")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен!")
    yield
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    await dp.feed_update(bot, types.Update(**update))


def main() -> None:
    dp.include_router(router)
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    main()
