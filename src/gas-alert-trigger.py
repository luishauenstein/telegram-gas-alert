import logging
from dotenv import load_dotenv
import os
import requests
from operator import and_
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import time

from schema import Alert


def main():

    load_dotenv()  # load .env files as env vars
    ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]

    # postgres connection
    postgres_url_string = "postgresql://postgres@localhost:5432/telegram-gas-alert"
    engine = create_engine(postgres_url_string, echo=False, future=True)

    current_timestamp = time.time()

    # get current gas price from Etherscan
    etherscan_endpoint = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(etherscan_endpoint)
        response.raise_for_status()
        data = response.json()
        current_gas = data["result"]["FastGasPrice"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except:
        raise SystemExit("Something went wrong.")

    # check DB for alerts where gas price is low enough and current time > timestamp
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


if __name__ == "__main__":
    main()
