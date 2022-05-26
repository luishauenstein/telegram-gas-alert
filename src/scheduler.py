from dotenv import load_dotenv
import os
import telebot
from sqlalchemy import create_engine, text

load_dotenv()  # load .env files as env vars
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM active_alerts"))
    for row in result:
        print(row)


bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    response = f"""
        Hi there! \n
        Your chat id: {message.chat.id} \n
    """
    bot.reply_to(message, response)


# def send_message():
#    chat_id = 1442097388
#    bot.send_message(chat_id, "The first message wow")
# send_message()


# bot.infinity_polling()
