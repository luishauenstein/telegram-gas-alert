from sqlalchemy import create_engine


from AlertSetup import AlertSetup
import global_variables as glb


# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)


def check_and_write_alert_to_db(alert: AlertSetup):
    chat_id = alert.chat_id
    if (
        glb.current_alert_setups[chat_id].cooldown_seconds != None
        and glb.current_alert_setups[chat_id].gas_threshold_gwei != None
    ):
        print("write alert to db")
        glb.current_alert_setups.pop(chat_id)
    pass
