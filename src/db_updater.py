from sqlalchemy import create_engine


from AlertSetup import AlertSetup


# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)


def write_alert_to_db(alert: AlertSetup):
    print("write alert to db")
    pass
