from typing import List

from fastapi import APIRouter

from routers.routes import chat_router
from routers.routes import connectivity_router


TAG_ROOT = "root"

router = APIRouter(prefix="/v1")

routers_to_include: List[APIRouter] = [
    # This is the order they show up in openapi.json
    chat_router.router,
    connectivity_router.router,
]

for router_to_include in routers_to_include:
    router.include_router(router_to_include)
