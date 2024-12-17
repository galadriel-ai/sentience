from fastapi import APIRouter
from fastapi import Depends

import dependencies
from service.tee.entities import GetSolanaPublicKeyResponse
from service.tee import get_solana_public_key

TAG = "TEE"
router = APIRouter(prefix="/tee")
router.tags = [TAG]


@router.get(
    "/public-key",
    summary="Get the Solana public key of the enclave",
    description="Get the Solana public key of the enclave",
    response_description="Returns a check connectivity response",
    response_model=GetSolanaPublicKeyResponse,
)
async def public_key(solana_client=Depends(dependencies.get_solana_client)):
    return await get_solana_public_key.execute(solana_client)
