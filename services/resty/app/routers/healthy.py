from fastapi import APIRouter, Response

import bl

packages_router = APIRouter()


@packages_router.post("/healthy/", tags=["healthy"])
async def send_request_to_healthy(packages: dict, response: Response):
    return bl.send_request_to_healthy(packages, response)
