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
    try:
        current_alert_setups[chat_id].try_parse_gas_threshold(user_input[1])
    except:
        pass
    try:
        current_alert_setups[chat_id].try_parse_cooldown(user_input[2])
    except:
        pass
    if current_alert_setups[chat_id].gas_threshold_gwei == None:
        bot.send_message(
            chat_id,
            "Please enter your target gas price that you want to be alerted at (must be between 1 and 9999):",
            reply_markup=telebot.types.ForceReply(
                input_field_placeholder="Gas threshold in Gwei (e.g. 15)"
            ),
        )
        return 0
    elif current_alert_setups[chat_id].cooldown_seconds == None:
        bot.send_message(
            chat_id,
            "Please tell me how many hours should at least be between each alert: (must be between 1 and 9999",
            reply_markup=telebot.types.ForceReply(
                input_field_placeholder="Alert cooldown in hours (e.g. 3)"
            ),
        )
        return 0
    else:
        bot.send_message(chat_id, "Awesome, alert has been set up!")
        print("set up alert")

    print(
        current_alert_setups[chat_id].chat_id,
        current_alert_setups[chat_id].gas_threshold_gwei,
        current_alert_setups[chat_id].cooldown_seconds,
    )


# handle digit input (for specifying gas and cooldown)
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
    pass


bot.infinity_polling()
