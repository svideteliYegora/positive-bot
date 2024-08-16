import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    TOKEN_API: str
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    WEBHOOK_URL: str
    WEBAPP_HOST: str
    WEBAPP_PORT: int


load_dotenv()
TOKEN_API = os.getenv('TOKEN_API')

# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

data = Settings(TOKEN_API, WEBHOOK_HOST, WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT)
