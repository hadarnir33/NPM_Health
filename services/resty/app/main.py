from fastapi import FastAPI

import routers

app = FastAPI()


app.include_router(routers.packages_router)
