from fastapi import APIRouter

import bl

packages_router = APIRouter()


@packages_router.post("/packages/", tags=["packages"])
async def check_health_of_packages():
    return bl.send_request_to_healthy()