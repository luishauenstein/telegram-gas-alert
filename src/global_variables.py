# namespace for global variables (shared across modules)

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import telebot

# dict that temp stores all alerts that are currently in the process of being set up
current_alert_setups = {}

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/postgres"
db_engine = create_engine(postgres_url_string, echo=False, future=True)

# load env vars
load_dotenv()  # load .env files as env vars
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

# set up telebot
bot = telebot.TeleBot(TELEGRAM_API_KEY)
