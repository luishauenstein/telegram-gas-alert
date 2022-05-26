from operator import and_
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import time

from schema import Alert

# postgres connection
postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
engine = create_engine(postgres_url_string, echo=False, future=True)


current_timestamp = time.time()
current_gas = 21  # example hardcoded value for now

stmt = select(Alert).where(
    and_(
        Alert.cooldown_expired_timestamp <= current_timestamp,
        Alert.gas_threshold_gwei <= current_gas,
    )
)
with Session(engine) as session:
    for row in session.execute(stmt):
        print(
            f"{row.Alert.alert_id} {row.Alert.gas_threshold_gwei} {row.Alert.cooldown_expired_timestamp}"
        )
        # 1. trigger alert
        # 2. update cooldown_expired_timestamp
