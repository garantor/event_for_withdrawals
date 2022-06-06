# This has to be run from a separate terminal


from stellar_sdk import AiohttpClient, ServerAsync
import asyncio
import requests
from decouple import config
import logging
logging.basicConfig(level=logging.INFO,  format="%(levelname)s %(message)s")

# withdrawal_address = "GBRUNBDAHPAPFGORNVH6AIFZKBV7252DEIEJULIB73QQJ4BLAOHGU57J"
withdrawal_address = config('WITHDRAWAL_ADDRESS')
HORIZON_URL = "https://horizon-testnet.stellar.org"

event_url = config("BASE_URL")
# event_url = "http://127.0.0.1:8000/listener" or "https://stablemvp.herokuapp.com/listener"

"""
Event listener listen for transactions on the stablecoin issuer address,
and when a payment transaction is received, it will send a POST request to the event_url
This is a user withdrawal transaction
"""


async def payments():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for transactions in server.transactions().for_account(withdrawal_address).stream():
            try:
                logging.info(transactions['hash'])
                logging.info(transactions['memo'])
                data = (
                    {"hash": transactions["hash"], "memo": transactions["memo"], "event_type": "user_withdrawals"})
                requests.post(event_url, data=data)
            except Exception as e:
                # Add a way to send notification for error to admin group
                logging.critical(e)
                continue




async def listen():
    await asyncio.gather(payments())


if __name__ == "__main__":
    logging.info("Event Listener Started.....")
    logging.info("listening for withdrawals.....")
    asyncio.run(listen())
