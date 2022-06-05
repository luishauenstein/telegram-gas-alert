import telebot


def handle_reply(bot, alert):
    # user has not entered gas threshold yet
    if alert.gas_threshold_gwei == None:
        bot.send_message(
            alert.chat_id,
            "Please enter your target gas price that you want to be alerted at (must be between 1 and 9999):",
            reply_markup=telebot.types.ForceReply(
                input_field_placeholder="Gas threshold in Gwei (e.g. 15)"
            ),
        )
        return 0

    # user has not entered cooldown yet
    elif alert.cooldown_seconds == None:
        bot.send_message(
            alert.chat_id,
            "Please tell me how many hours should at least be between each alert (must be between 1 and 9999):",
            reply_markup=telebot.types.ForceReply(
                input_field_placeholder="Alert cooldown in hours (e.g. 3)"
            ),
        )
        return 0

    # user has entered both
    else:
        bot.send_message(alert.chat_id, "Awesome, alert has been set up!")
