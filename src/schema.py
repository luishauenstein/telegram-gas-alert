from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import declarative_base

import global_variables as glb

Base = declarative_base()


class Alert(Base):
    __tablename__ = "active_alerts"
    alert_id = Column(BigInteger, primary_key=True)
    telegram_chat_id = Column(BigInteger, nullable=False)
    gas_threshold_gwei = Column(Integer, nullable=False)
    cooldown_seconds = Column(Integer, nullable=False)
    cooldown_expired_timestamp = Column(BigInteger, nullable=False)


Base.metadata.create_all(glb.db_engine)
