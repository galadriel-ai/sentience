import asyncio

from proxy_checks import galadriel_call
from proxy_checks import google_serper_call
from proxy_checks import openai_call


async def main():
    print("\n=== OPENAI call start ===")
    openai_is_success, openai_error = openai_call.execute()
    print("=== OPENAI Call done ===")
    print("\n=== GoogleSerper call start ===")
    serper_is_success, serper_error = await google_serper_call.execute()
    print("=== GoogleSerper call done ===")
    print("\n=== Galadriel call start ===")
    galadriel_is_success, galadriel_error = await galadriel_call.execute()
    print("=== Galadriel call done ===")

    print("\nChecking proxies:")
    print(f"  OpenAI success={openai_is_success}, error={openai_error}")
    print(f"  Serper success={serper_is_success}, error={serper_error}")
    print(f"  Galadriel success={galadriel_is_success}, error={galadriel_error}")
    print("\n")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as exc:
        print("Exception in check proxies:", exc)
