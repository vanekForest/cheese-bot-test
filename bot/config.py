import logging
import os
import json

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

if os.getenv("local") == "true":
    storage = MemoryStorage()
else:
    storage = RedisStorage.from_url("redis://redis:6379/1")

logging.basicConfig(level=logging.INFO)
__log__ = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("token")
IMAGES_PATH = "jsons/images.json"
MESSAGES = json.load(open("jsons/message.json", encoding="utf-8"))
BUTTONS = json.load(open("jsons/button.json", encoding="utf-8"))
IMAGES = json.load(open(IMAGES_PATH, encoding="utf-8"))
URLS = json.load(open("jsons/url.json", encoding="utf-8"))
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
PRICES = json.load(open("jsons/prices.json", encoding="utf-8"))
CHANNEL_ID = os.getenv("channel_id")
POST_SCHEDULED_TASK_INTERVAL = 60 * 15
SUBSCRIBE_SCHEDULED_TASK_INTERVAL = 60 * 24
SALE_OFFER_SCHEDULED_TASK_INTERVAL = 60 * 16
