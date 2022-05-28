import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_APP_API_ID = os.environ.get("TELEGRAM_APP_API_ID")
TELEGRAM_APP_API_HASH = os.environ.get("TELEGRAM_APP_API_HASH")
VK_TOKEN = os.environ.get("VK_TOKEN")
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_DATABASE = os.environ.get("DATABASE_DATABASE")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

VK_API_VERSION = "5.100"
