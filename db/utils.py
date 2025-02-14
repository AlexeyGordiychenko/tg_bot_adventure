import logging
import os

from config import GAME_DB_PATH

from db.load_all import load_all


def check_db() -> None:
    if not os.path.exists(GAME_DB_PATH):
        logging.info(f"Database not found, creating {GAME_DB_PATH} ...")
        load_all()
    else:
        logging.info(f"Database found: {GAME_DB_PATH}")
