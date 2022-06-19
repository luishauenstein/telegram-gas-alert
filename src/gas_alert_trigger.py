import requests
import time
from operator import and_

from sqlalchemy import select

from database_schema import Alert
import global_variables as glb


def main():
    current_timestamp = time.time()

    # get current gas price from Etherscan
    etherscan_endpoint = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={glb.ETHERSCAN_API_KEY}"
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
            Alert.gas_threshold_gwei >= current_gas,
        )
    )
    with glb.Session() as session:
        for row in session.execute(stmt):
            alert: Alert = row.Alert
            try:
                # 1. trigger alert
                message = (
                    f"Gas alert triggered! ⛽\nCurrent gas price: *{current_gas} Gwei*"
                )
                glb.bot.send_message(
                    alert.telegram_chat_id, message, parse_mode="Markdown"
                )
                # 2. update cooldown_expired_timestamp
                alert.cooldown_expired_timestamp = time.time() + alert.cooldown_seconds
                session.commit()
            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
