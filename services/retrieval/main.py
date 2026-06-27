from app.api.main import app
from ingest_routes import router

app.include_router(router)
