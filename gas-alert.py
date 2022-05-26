from dotenv import load_dotenv
import os
import telebot
import sqlalchemy

load_dotenv()  # load .env files as env vars

# postgres connection
engine = sqlalchemy.create_engine(
    "postgresql://user@localhost:5432", echo=True, future=True
)
print(engine)

# telegram servers connection
API_TOKEN = os.environ["TELEGRAM_API_KEY"]
bot = telebot.TeleBot(API_TOKEN)

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
