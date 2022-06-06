from dotenv import load_dotenv
import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from AlertSetup import AlertSetup
from schema import Alert
import global_variables as glb

load_dotenv()  # load .env files as env vars
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)


bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome_help(message):
    response = "Hi there! 👋\nFollowing commands are available:\n\n`/gas-alert [price Gwei] [cooldown hours]` to set an alert\n`/show-alerts` to display and delete alerts\n`/about` to get info about this bot"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


# Handle '/info' and '/about'
@bot.message_handler(commands=["about", "info"])
def handle_about(message):
    bot.send_message(
        message.chat.id,
        "Created in 2022 by [Luis](https://twitter.com/luishauenstein).\nYou can find the code on [GitHub](https://github.com/luishauenstein/telegram-gas-alert).",
        disable_web_page_preview=True,
        parse_mode="Markdown",
    )


# Handle '/show-alerts'
@bot.message_handler(
    commands=[
        "showalerts",
        "showalert",
        "show-alerts",
        "show-alert",
        "show_alerts",
        "show_alert",
    ]
)
def handle_show_alerts(message):
    chat_id = message.chat.id
    # get active alerts from db
    stmt = select(Alert).where(
        Alert.telegram_chat_id <= chat_id,
    )
    active_alerts_inline_keyboard = []
    with Session(engine) as session:
        for row in session.execute(stmt):
            alert: Alert = row.Alert
            cooldown_hours = alert.cooldown_seconds // 3600
            text = f"Price: {alert.gas_threshold_gwei} Gwei      Cooldown: {cooldown_hours}h"
            active_alerts_inline_keyboard.append(
                [InlineKeyboardButton(text=text, callback_data=alert.alert_id)]
            )
    bot.send_message(
        chat_id,
        "Your notices (Click on one to delete it):",
        reply_markup=InlineKeyboardMarkup(active_alerts_inline_keyboard),
    )


# handle callback query after user clicks on an alert under '/show-alerts'
@bot.callback_query_handler(func=lambda call: True)
def delete_callback(call):
    alert_id = call.data
    chat_id = call.message.chat.id
    # drop selected alert
    with Session(engine) as session:
        try:
            alert_to_delete = session.get(Alert, alert_id)
            session.delete(alert_to_delete)
            session.commit()
            bot.send_message(chat_id, "Alert deleted.")
        except Exception as err:
            print(err)
    # inform user about deleted alert
    bot.answer_callback_query(call.id)


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
    if chat_id not in glb.current_alert_setups:
        bot.send_message(
            chat_id,
            "Welcome! Please use `/help` or `/start` to get started.",
            parse_mode="Markdown",
        )
        return 0
    alert: AlertSetup = glb.current_alert_setups[chat_id]
    if alert.gas_threshold_gwei == None:
        alert.try_parse_gas_threshold(message.text)
    elif alert.cooldown_seconds == None:
        alert.try_parse_cooldown(message.text)
    alert.handle_reply(bot)
    alert.check_and_write_alert_to_db()


bot.infinity_polling()
