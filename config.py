import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(','))) if os.getenv("ADMIN_IDS") else []