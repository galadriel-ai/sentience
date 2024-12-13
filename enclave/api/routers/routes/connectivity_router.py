from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request

import dependencies
from service.connectivity.entities import CheckConnectivityResponse
from service.connectivity import check_connectivity_service

TAG = "Connectivity"
router = APIRouter(prefix="/connectivity")
router.tags = [TAG]


@router.get(
    "/",
    summary="Checks Enclave connectivity to external services",
    description="Checks Enclave connectivity to external services",
    response_description="Returns a check connectivity response",
    response_model=CheckConnectivityResponse,
)
async def completions():
    return await check_connectivity_service.execute()
