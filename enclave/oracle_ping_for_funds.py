import asyncio
import time

from web3 import AsyncWeb3

import settings
import key_manager

web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_RPC_URL))

account = key_manager.get_account()


async def get_balance():
    balance = await web3_client.eth.get_balance(account.address)
    return balance


async def main():
    while True:
        balance = await get_balance()
        print(f"Address: {account.address}, balance: {balance}")
        if balance > 0:
            print("\nSuccess, got funds!")
            return

        time.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
