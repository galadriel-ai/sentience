import httpx

from service.connectivity.entities import CheckConnectivityResponse


async def execute() -> CheckConnectivityResponse:
    return CheckConnectivityResponse(
        openai=await _check_connectivity("https://api.openai.com/", 421),
        solana_mainnet=await _check_connectivity(
            "https://api.mainnet-beta.solana.com/", 200
        ),
        solana_devnet=await _check_connectivity("https://api.devnet.solana.com/", 200),
    )


async def _check_connectivity(url: str, expected_response: int) -> bool:
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            response = await client.get(url)
            return response.status_code == expected_response
    except Exception:
        return False
