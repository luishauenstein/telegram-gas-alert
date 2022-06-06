# namespace for global variables (shared across modules)

from sqlalchemy import create_engine

# dict that temp stores all alerts that are currently in the process of being set up
current_alert_setups = {}

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
db_engine = create_engine(postgres_url_string, echo=False, future=True)
