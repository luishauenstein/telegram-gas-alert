from dotenv import load_dotenv
import os
import telebot
from sqlalchemy import create_engine

from AlertSetup import AlertSetup

load_dotenv()  # load .env files as env vars
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)

bot = telebot.TeleBot(TELEGRAM_API_KEY)

current_alert_setups = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome_help(message):
    response = f"""
        Hi there! \n
        Your chat id: {message.chat.id} \n
    """
    bot.reply_to(message, response)


# Handle '/gas-alert' (allows user to create new alert)
@bot.message_handler(
    commands=[
        "gasalert",
        "gas-alert",
        "gas_alert",
        "setalert",
        "set-alert",
        "set_alert",
        "createalert",
        "create-alert",
        "create_alert",
    ]
)
def handle_set_alert_command(message):
    chat_id = message.chat.id
    user_input = message.text.split()[:3]
    current_alert_setups[chat_id] = AlertSetup(chat_id)
    print(
        current_alert_setups[chat_id].chat_id,
        current_alert_setups[chat_id].gas_threshold_gwei,
        current_alert_setups[chat_id].cooldown_seconds,
    )
    bot.reply_to(
        message,
        "message received",
        reply_markup=telebot.types.ForceReply(input_field_placeholder="Gas price"),
    )


bot.infinity_polling()
