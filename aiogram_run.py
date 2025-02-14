from contextlib import asynccontextmanager
import logging
import os
from fastapi import FastAPI
from aiogram import types
import uvicorn
from create_bot import (
    bot,
    dp,
    BASE_URL,
    WEBHOOK_PATH,
    HOST,
    PORT,
    ADMIN_ID,
    GAME_DB_PATH,
)
from handlers import router
from aiogram.types import BotCommand, BotCommandScopeDefault
from load_all import load_all


async def set_commands():
    commands = [BotCommand(command="start", description="Start you adventure")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен!")
    yield
    if ADMIN_ID:
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
    if not os.path.exists(GAME_DB_PATH):
        logging.info(f"Database not found, creating {GAME_DB_PATH} ...")
        load_all()
    else:
        logging.info(f"Database found: {GAME_DB_PATH}")

    main()
