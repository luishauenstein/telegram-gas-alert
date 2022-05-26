from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from schema import Alert

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)

stmt = select(Alert).where(Alert.cooldown_seconds <= 2000)
with Session(engine) as session:
    for row in session.execute(stmt):
        print(f"{row.Alert.alert_id} {row.Alert.cooldown_seconds}")
