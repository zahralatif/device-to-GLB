from pathlib import Path

from app.core.config import settings


STORAGE_ROOT = Path(settings.STORAGE_PATH)

ORIGINAL_ROOT = STORAGE_ROOT / "originals"
PREPARED_ROOT = STORAGE_ROOT / "prepared"
GLB_ROOT = STORAGE_ROOT / "glb"
GENERATED_ROOT = STORAGE_ROOT / "generated"


for root in (
    STORAGE_ROOT,
    ORIGINAL_ROOT,
    PREPARED_ROOT,
    GLB_ROOT,
    GENERATED_ROOT,
):
    root.mkdir(parents=True, exist_ok=True)