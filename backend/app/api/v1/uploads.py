from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.schemas.upload import UploadResponse
from app.services.upload_service import save_upload

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)


@router.post("/", response_model=UploadResponse)
def upload_image(
    file: UploadFile = File(...)
):
    path = save_upload(file)

    return UploadResponse(
        filename=Path(path).name,
        path=path,
    )