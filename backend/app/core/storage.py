from pathlib import Path

from app.core.config import settings


STORAGE_ROOT = Path(settings.STORAGE_PATH)
UPLOAD_ROOT = Path(settings.UPLOAD_PATH)

STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)