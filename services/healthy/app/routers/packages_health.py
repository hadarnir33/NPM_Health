from fastapi import APIRouter

import bl
import models

packages_router = APIRouter()


@packages_router.post("/packages/", tags=["packages"])
async def check_health_of_packages(packages: models.Packages):
    return bl.check_health_of_packages(packages)
