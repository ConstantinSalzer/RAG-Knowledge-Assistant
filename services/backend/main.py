from fastapi import FastAPI

from services.backend.routes import router

app = FastAPI()

app.include_router(router)