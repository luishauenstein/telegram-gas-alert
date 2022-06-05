from dotenv import load_dotenv
import os
import telebot

from AlertSetup import AlertSetup
import global_variables as glb

load_dotenv()  # load .env files as env vars
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]


bot = telebot.TeleBot(TELEGRAM_API_KEY)

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
    alert = glb.current_alert_setups[chat_id] = AlertSetup(chat_id)
    if len(user_input) >= 2:
        alert.try_parse_gas_threshold(user_input[1])
    if len(user_input) >= 3:
        alert.try_parse_cooldown(user_input[2])
    alert.handle_reply(bot)
    alert.check_and_write_alert_to_db()


# handle digit input (for specifying gas and cooldown)
@bot.message_handler(content_types=["text"])
def handle_message(message):
    chat_id = message.chat.id
    alert: AlertSetup = glb.current_alert_setups[chat_id]
    if chat_id not in glb.current_alert_setups:
        bot.send_message(chat_id, "Welcome! Please use /help or /start to get started.")
        return 0
    elif alert.gas_threshold_gwei == None:
        alert.try_parse_gas_threshold(message.text)
    elif alert.cooldown_seconds == None:
        alert.try_parse_cooldown(message.text)
    alert.handle_reply(bot)
    alert.check_and_write_alert_to_db()


bot.infinity_polling()
