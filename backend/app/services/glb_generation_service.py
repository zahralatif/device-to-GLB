from pathlib import Path
import shutil

from app.core.storage import PREPARED_ROOT, GLB_ROOT


def generate_glb(model_id: str) -> str:
    """
    Temporary GLB generator.

    Future implementation:
        Agglogic / Blender

    Current implementation:
        creates a placeholder .glb file.
    """

    GLB_ROOT.mkdir(parents=True, exist_ok=True)

    glb_path = GLB_ROOT / f"{model_id}.glb"

    with open(glb_path, "wb") as f:
        f.write(b"")

    return str(glb_path)