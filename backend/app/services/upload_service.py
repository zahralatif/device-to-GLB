from pathlib import Path
import shutil

from fastapi import UploadFile

from app.core.storage import ORIGINAL_ROOT

def save_upload(
    model_id: str,
    face: str,
    file: UploadFile,
) -> str:

    VALID_FACES = {
        "front",
        "rear",
        "left",
        "right",
        "top",
        "bottom",
    }

    if face not in VALID_FACES:
        raise ValueError(f"Invalid face: {face}")

    folder = ORIGINAL_ROOT / model_id
    folder.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix or ".png"

    destination = folder / f"{face}{extension}"

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return str(destination)