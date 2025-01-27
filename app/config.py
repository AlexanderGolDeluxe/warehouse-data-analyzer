from pathlib import Path

from environs import Env
from loguru import logger

ENV = Env(expand_vars=True)
ENV.read_env()

API_PREFIX = ENV.str("API_PREFIX")
BASE_DIR = Path(__file__).parent.parent
DEBUG_MODE = ENV.bool("DEBUG_MODE")
DB_URL = (
    Path(f"{BASE_DIR}/app/db").mkdir(parents=True, exist_ok=True) or
    f"sqlite+aiosqlite:///{BASE_DIR}/app/db/{BASE_DIR.stem}.sqlite3"
)
INVENTORY_CREATION_QUEUE_NAME = ENV.str("INVENTORY_CREATION_QUEUE_NAME")
HANDLER_INVENTORY_CREATION_INTERVAL = ENV.int(
    "HANDLER_INVENTORY_CREATION_INTERVAL"
)
RMQ_URL = ENV.str("RMQ_URL")

logger.add(
    f"{BASE_DIR}/app/logs/{BASE_DIR.stem}_app.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 day",
    retention="7 days")
