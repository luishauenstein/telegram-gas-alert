# namespace for global variables (shared across modules)

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import telebot

# load env vars
load_dotenv()  # load .env files as env vars
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

# postgres connection
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PW = os.environ["POSTGRES_PW"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DBNAME = os.environ["POSTGRES_DBNAME"]
postgres_url_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"  # postgresql://[user[:password]@][netloc][:port][/dbname]
db_engine = create_engine(postgres_url_string, echo=False, future=True)

# set up telebot
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# dict that temp stores all alerts that are currently in the process of being set up
current_alert_setups = {}
