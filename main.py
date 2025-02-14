import logging

import uvicorn
from api import app
from bot import dp
from bot.handlers import router
from config import HOST, PORT
from db.utils import check_db

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    check_db()
    dp.include_router(router)
    uvicorn.run(app, host=HOST, port=PORT)
