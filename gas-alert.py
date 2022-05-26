from dotenv import load_dotenv
import os
import telebot

load_dotenv()  # load .env files as env vars

API_TOKEN = os.environ["TELEGRAM_API_KEY"]
print(API_TOKEN)

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(message, "Hi there, I am the ETH gas bot!")


bot.infinity_polling()
