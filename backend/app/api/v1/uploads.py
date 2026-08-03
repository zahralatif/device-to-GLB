from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.upload import UploadResponse
from app.services.upload_service import save_upload

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)


@router.post("/{face}", response_model=UploadResponse)
def upload_image(
    face: str,
    file: UploadFile = File(...),
):
    try:
        path = save_upload(file, face)

        return UploadResponse(
            filename=path.split("/")[-1],
            path=path,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )