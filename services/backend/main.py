from fastapi import FastAPI

from services.backend.db import init_db
from services.backend.routes import router

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    # Erstellt die conversations-Tabelle beim Start, falls sie noch nicht existiert.
    init_db()


app.include_router(router)
