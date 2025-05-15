import json
import logging
from contextlib import asynccontextmanager

from aiogram import types
from bot import bot, dp, set_commands
from config import ADMIN_ID, BASE_URL, WEBHOOK_PATH
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_commands()
    # urljoin doesn't work on the server for some reason, so I use manual concatenation here
    await bot.set_webhook(f"{BASE_URL.rstrip('/')}/{WEBHOOK_PATH.lstrip('/')}")
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text="Bot's started")
    yield
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text="Bot's stopped")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)


@app.post(f"/{WEBHOOK_PATH.lstrip()}")
async def bot_webhook(update: dict):
    logger.info(json.dumps(update))
    if "message" in update and "chat" in update["message"]:
        if str(update["message"]["chat"]["id"]) != ADMIN_ID:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Interaction received from id={update['message']['chat']['id']}; user={update['message']['chat']['username']}",
            )
    await dp.feed_update(bot, types.Update(**update))
