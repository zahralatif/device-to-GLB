#!/usr/bin/env python3
"""
device-to-glb.py — Generate a 6-face textured GLB model from device images.

Part of the MIDA-HMON 3D Asset Pipeline.
See: MIDA-HMON-3DAssetCreation-Guide.md for full workflow.

Usage:
    python3 device-to-glb.py \
        --id switch-2u-cisco-9300 \
        --width 443 --depth 450 --height 88 \
        --front ref/cisco-9300-front.png \
        --rear  ref/cisco-9300-rear.png \
        --left  ref/cisco-9300-left.png \
        --right ref/cisco-9300-right.png \
        --top   ref/cisco-9300-top.png \
        --color '#1a1a2e' \
        --output models/switch-2u-cisco-9300.glb

Dependencies: pip install trimesh Pillow numpy
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image


# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

FACES = ("front", "rear", "left", "right", "top", "bottom")

# Default body colour when no image is provided for a face
DEFAULT_BODY_COLOR = "#444444"

# Recommended image dimensions (pixels) per device form factor
RECOMMENDED_RESOLUTIONS = {
    "1U":  (1024, 256),
    "2U":  (1024, 512),
    "4U":  (1024, 1024),
    "PDU": (256, 2048),
}

# PBR material defaults
PBR_TEXTURED = {"metallicFactor": 0.1, "roughnessFactor": 0.8}
PBR_SOLID    = {"metallicFactor": 0.3, "roughnessFactor": 0.6}


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def hex_to_rgba(hex_str: str) -> list:
    """Convert '#RRGGBB' to [r, g, b, a] in 0-255 range."""
    h = hex_str.lstrip("#")
    return [int(h[i:i+2], 16) for i in (0, 2, 4)] + [255]


def solid_color_image(width: int, height: int, hex_color: str) -> Image.Image:
    """Create a solid-colour image for faces without a texture."""
    rgba = hex_to_rgba(hex_color)
    img = Image.new("RGBA", (width, height), tuple(rgba))
    return img


def load_face_image(path: str | None, face_width_mm: float,
                    face_height_mm: float, body_color: str) -> Image.Image:
    """Load an image from path, or generate a solid-colour fallback."""
    if path and Path(path).is_file():
        img = Image.open(path).convert("RGBA")
        # Warn if aspect ratio is significantly off
        img_ratio = img.width / img.height
        face_ratio = face_width_mm / face_height_mm
        if abs(img_ratio - face_ratio) / face_ratio > 0.15:
            print(f"  WARNING: Image {Path(path).name} aspect ratio "
                  f"({img_ratio:.2f}) differs from face ({face_ratio:.2f}) "
                  f"by >{15}%. Image will be stretched to fit.")
        return img
    # No image — return solid colour
    # Use a small resolution for solid faces (saves file size)
    return solid_color_image(64, 64, body_color)


def create_face_mesh(width: float, height: float, depth: float,
                     face: str, image: Image.Image) -> trimesh.Trimesh:
    """
    Create a single-quad mesh for one face of the device box.

    Coordinate convention (matches agglogic scene3d):
        +X = right
        +Y = forward (depth, into rack)
        +Z = up
        Origin = geometric centre of box

    UV mapping: image fills the face naturally when viewed from outside.
    """
    hw, hh, hd = width / 2, height / 2, depth / 2

    # Each face: 4 vertices, 2 triangles, UV-mapped for natural viewing
    face_defs = {
        # Front: Y = -hd, normal (0, -1, 0)
        # Viewed from front: left=-X, right=+X, bottom=-Z, top=+Z
        "front": {
            "vertices": [
                [-hw, -hd, -hh],  # bottom-left
                [ hw, -hd, -hh],  # bottom-right
                [ hw, -hd,  hh],  # top-right
                [-hw, -hd,  hh],  # top-left
            ],
            "normal": [0, -1, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        # Rear: Y = +hd, normal (0, 1, 0)
        # Viewed from rear: mirrored X axis
        "rear": {
            "vertices": [
                [ hw, hd, -hh],
                [-hw, hd, -hh],
                [-hw, hd,  hh],
                [ hw, hd,  hh],
            ],
            "normal": [0, 1, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        # Left: X = -hw, normal (-1, 0, 0)
        # Viewed from left: rear edge at left, front at right
        "left": {
            "vertices": [
                [-hw,  hd, -hh],
                [-hw, -hd, -hh],
                [-hw, -hd,  hh],
                [-hw,  hd,  hh],
            ],
            "normal": [-1, 0, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        # Right: X = +hw, normal (1, 0, 0)
        # Viewed from right: front edge at left, rear at right
        "right": {
            "vertices": [
                [hw, -hd, -hh],
                [hw,  hd, -hh],
                [hw,  hd,  hh],
                [hw, -hd,  hh],
            ],
            "normal": [1, 0, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        # Top: Z = +hh, normal (0, 0, 1)
        # Viewed from above: front at bottom, rear at top
        "top": {
            "vertices": [
                [-hw, -hd, hh],
                [ hw, -hd, hh],
                [ hw,  hd, hh],
                [-hw,  hd, hh],
            ],
            "normal": [0, 0, 1],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        # Bottom: Z = -hh, normal (0, 0, -1)
        "bottom": {
            "vertices": [
                [-hw,  hd, -hh],
                [ hw,  hd, -hh],
                [ hw, -hd, -hh],
                [-hw, -hd, -hh],
            ],
            "normal": [0, 0, -1],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
    }

    fd = face_defs[face]
    vertices = np.array(fd["vertices"], dtype=np.float64)
    faces_idx = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    normals = np.tile(fd["normal"], (4, 1)).astype(np.float64)

    # Create material with texture
    material = trimesh.visual.material.PBRMaterial(
        baseColorTexture=image,
        metallicFactor=PBR_TEXTURED["metallicFactor"] if image.size[0] > 64 else PBR_SOLID["metallicFactor"],
        roughnessFactor=PBR_TEXTURED["roughnessFactor"] if image.size[0] > 64 else PBR_SOLID["roughnessFactor"],
    )

    uv = np.array(fd["uv"], dtype=np.float64)

    visual = trimesh.visual.TextureVisuals(uv=uv, material=material)
    mesh = trimesh.Trimesh(
        vertices=vertices,
        faces=faces_idx,
        vertex_normals=normals,
        visual=visual,
        process=False,
    )
    return mesh


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Generate a 6-face textured GLB device model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full 6-face model
  python3 device-to-glb.py \\
      --id switch-2u-cisco-9300 \\
      --width 443 --depth 450 --height 88 \\
      --front ref/front.png --rear ref/rear.png \\
      --left ref/side.png --right ref/side.png \\
      --top ref/top.png --color '#1a1a2e' \\
      --output models/switch-2u-cisco-9300.glb

  # Front-only (minimum viable model)
  python3 device-to-glb.py \\
      --id ups-3u-apc \\
      --width 443 --depth 660 --height 132 \\
      --front ref/apc-ups-front.png \\
      --output models/ups-3u-apc.glb

  # Symmetric device (left = right)
  python3 device-to-glb.py \\
      --id server-1u-dell-r650 \\
      --width 443 --depth 734 --height 43 \\
      --front ref/dell-r650-front.png \\
      --rear ref/dell-r650-rear.png \\
      --left ref/dell-r650-side.png \\
      --right ref/dell-r650-side.png \\
      --output models/server-1u-dell-r650.glb
        """,
    )
    parser.add_argument("--id", required=True, help="Model ID (e.g. switch-2u-cisco-9300)")
    parser.add_argument("--width", type=float, required=True, help="Device width in mm")
    parser.add_argument("--depth", type=float, required=True, help="Device depth in mm")
    parser.add_argument("--height", type=float, required=True, help="Device height in mm")
    parser.add_argument("--front", help="Front face image (PNG/JPEG)")
    parser.add_argument("--rear", help="Rear face image (PNG/JPEG)")
    parser.add_argument("--left", help="Left face image (PNG/JPEG)")
    parser.add_argument("--right", help="Right face image (PNG/JPEG)")
    parser.add_argument("--top", help="Top face image (PNG/JPEG)")
    parser.add_argument("--bottom", help="Bottom face image (PNG/JPEG)")
    parser.add_argument("--color", default=DEFAULT_BODY_COLOR,
                        help=f"Body colour hex (default: {DEFAULT_BODY_COLOR})")
    parser.add_argument("--output", required=True, help="Output GLB file path")
    parser.add_argument("--manifest", help="Path to manifest.json to update")

    args = parser.parse_args()

    face_paths = {
        "front": args.front, "rear": args.rear,
        "left": args.left, "right": args.right,
        "top": args.top, "bottom": args.bottom,
    }

    # Validate at least one face
    provided = [f for f, p in face_paths.items() if p and Path(p).is_file()]
    if not provided:
        print("ERROR: At least one face image is required (--front recommended).")
        sys.exit(1)

    # Face dimensions for each face (width × height of the face rectangle in mm)
    face_dims = {
        "front":  (args.width, args.height),
        "rear":   (args.width, args.height),
        "left":   (args.depth, args.height),
        "right":  (args.depth, args.height),
        "top":    (args.width, args.depth),
        "bottom": (args.width, args.depth),
    }

    print(f"\n{'═' * 56}")
    print(f" DEVICE MODEL GENERATOR")
    print(f"{'═' * 56}")
    print(f"  Model ID:    {args.id}")
    print(f"  Dimensions:  {args.width} × {args.depth} × {args.height} mm (W×D×H)")
    print(f"  Body colour: {args.color}")
    print()

    # Convert mm to metres for glTF
    w_m = args.width / 1000
    d_m = args.depth / 1000
    h_m = args.height / 1000

    # Build 6 face meshes
    meshes = []
    for face in FACES:
        fw, fh = face_dims[face]
        img = load_face_image(face_paths[face], fw, fh, args.color)
        status = f"{Path(face_paths[face]).name}" if face_paths[face] and Path(face_paths[face]).is_file() else "(body colour)"
        print(f"  {face:8s}  {status}")
        mesh = create_face_mesh(w_m, h_m, d_m, face, img)
        meshes.append(mesh)

    # Combine into single scene and export
    scene = trimesh.Scene(meshes)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    scene.export(args.output, file_type="glb")

    file_size = Path(args.output).stat().st_size
    print(f"\n  Output:      {args.output}")
    print(f"  File size:   {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    # Update manifest if specified
    if args.manifest and Path(args.manifest).is_file():
        manifest = json.loads(Path(args.manifest).read_text())
        entry = {
            "id": args.id,
            "file": Path(args.output).name,
            "category": "device",
            "source": "device-to-glb",
            "license": "internal",
            "dimensions_mm": {
                "width": args.width,
                "depth": args.depth,
                "height": args.height,
            },
            "faces_textured": provided,
            "generated_at": "2026-04-30",
        }
        existing = next((i for i, m in enumerate(manifest["models"]) if m["id"] == args.id), None)
        if existing is not None:
            manifest["models"][existing] = entry
            print(f"  Manifest:    UPDATED entry for {args.id}")
        else:
            manifest["models"].append(entry)
            manifest["models"].sort(key=lambda m: m["id"])
            print(f"  Manifest:    ADDED entry for {args.id}")
        Path(args.manifest).write_text(json.dumps(manifest, indent=2) + "\n")
    elif args.manifest:
        print(f"  Manifest:    {args.manifest} not found — skipped")

    print(f"\n  Associate with device:")
    print(f'    curl -X PUT .../api/devices/{{id}} -d \'{{"model_id":"{args.id}"}}\'')
    print(f"{'═' * 56}\n")


if __name__ == "__main__":
    main()
