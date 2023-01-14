from fastapi import APIRouter

import bl
import models

packages_router = APIRouter()


@packages_router.post("/packages/", tags=["packages"])
async def check_health_of_packages(packages_list: models.Packages):
    return bl.send_request_to_healthy(packages_list)