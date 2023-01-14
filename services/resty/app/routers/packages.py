from fastapi import APIRouter

import bl
import models

packages_router = APIRouter()


@packages_router.post("/packages/", tags=["packages"])
async def send_request_to_healthy(packages_list: models.Packages):
    return bl.send_request_to_healthy(packages_list)