from pathlib import Path
import shutil

from app.core.storage import PREPARED_ROOT


def prepare_image(
    model_id: str,
    face: str,
    original_path: str,
) -> str:
    """
    Temporary implementation.

    Currently just copies the original image into the
    prepared folder.

    Future:
    - background removal
    - resize
    - padding
    - normalization
    """

    destination_dir = PREPARED_ROOT / model_id
    destination_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(original_path).suffix

    destination = destination_dir / f"{face}{extension}"

    shutil.copy2(
        original_path,
        destination,
    )

    return str(destination)