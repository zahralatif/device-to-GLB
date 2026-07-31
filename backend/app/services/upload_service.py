from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile

from app.core.storage import UPLOAD_ROOT


def save_upload(file: UploadFile) -> str:
    extension = Path(file.filename).suffix.lower()

    filename = f"{uuid4().hex}{extension}"

    destination = UPLOAD_ROOT / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(destination)