from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.health import router as health_router
from app.api.v1.vendors import router as vendor_router
from app.api.v1.device_types import router as device_type_router
from app.api.v1.models import router as model_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.uploads import router as upload_router

from app.db.session import SessionLocal
from app.services.device_type_seed import seed_device_types

from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        "http://localhost:5557",
        "http://127.0.0.1:5557",

        "https://3dmodeller-srv01.dci.internal",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    db = SessionLocal()

    try:
        seed_device_types(db)
    finally:
        db.close()

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    vendor_router,
    prefix="/api/v1",
)

app.include_router(
    device_type_router,
    prefix="/api/v1",
)

app.include_router(
    model_router,
    prefix="/api/v1",
)

app.include_router(
    catalog_router,
    prefix="/api/v1",
)

app.include_router(
    upload_router,
    prefix="/api/v1",
)

app.mount(
    "/storage",
    StaticFiles(directory="storage"),
    name="storage",
)