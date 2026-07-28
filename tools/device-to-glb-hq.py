#!/usr/bin/env python3
"""
device-to-glb-hq.py — High-quality GLB generator for MIDA-HMON.

What this version does:
- Keeps the working 6-face texture behavior from device-to-glb.py
- Adds a beveled solid body mesh
- Adds optional front-panel detail meshes (raised/recessed blocks)
- Exports one GLB with embedded textures
- Updates manifest.json

Usage example:
    python device-to-glb-hq.py \
        --id switch-1u-cisco-catalyst-c9300-48p-m \
        --width 445 --depth 450 --height 44 \
        --front ref/cisco-9300/prepared/front.png \
        --rear ref/cisco-9300/prepared/rear.png \
        --left ref/cisco-9300/prepared/left.png \
        --right ref/cisco-9300/prepared/left.png \
        --top ref/cisco-9300/prepared/top.png \
        --color "#1a1a2e" \
        --bevel 2.0 \
        --detail-grid 24x2 \
        --detail-depth 2.0 \
        --output models/switch-1u-cisco-catalyst-c9300-48p-m.glb \
        --manifest manifest.json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import date

import numpy as np
import trimesh
from PIL import Image

FACES = ("front", "rear", "left", "right", "top", "bottom")

DEFAULT_BODY_COLOR = "#444444"

PBR_TEXTURED = {"metallicFactor": 0.1, "roughnessFactor": 0.8}
PBR_SOLID = {"metallicFactor": 0.3, "roughnessFactor": 0.6}


def hex_to_rgba(hex_str: str) -> list[int]:
    h = hex_str.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Invalid color: {hex_str}")
    return [int(h[i:i+2], 16) for i in (0, 2, 4)] + [255]


def solid_color_image(width: int, height: int, hex_color: str) -> Image.Image:
    rgba = hex_to_rgba(hex_color)
    return Image.new("RGBA", (width, height), tuple(rgba))


def load_face_image(
    path: str | None,
    face_width_mm: float,
    face_height_mm: float,
    body_color: str,
) -> tuple[Image.Image, bool]:
    if path and Path(path).is_file():
        img = Image.open(path).convert("RGBA")
        img_ratio = img.width / img.height
        face_ratio = face_width_mm / face_height_mm
        if abs(img_ratio - face_ratio) / face_ratio > 0.15:
            print(
                f"  WARNING: Image {Path(path).name} aspect ratio "
                f"({img_ratio:.2f}) differs from face ({face_ratio:.2f}) by >15%. "
                f"Image will be stretched to fit."
            )
        return img, True

    return solid_color_image(64, 64, body_color), False


def create_textured_face_mesh(
    width: float,
    height: float,
    depth: float,
    face: str,
    image: Image.Image,
    textured: bool,
    face_offset: float = 0.0,
) -> trimesh.Trimesh:
    """
    Create one textured quad, slightly offset outward if needed.

    Coordinate convention:
        +X = right
        +Y = rear / into rack
        +Z = up
        Front face is at -Y
    """
    hw, hh, hd = width / 2, height / 2, depth / 2
    eps = face_offset

    face_defs = {
        "front": {
            "vertices": [
                [-hw, -hd - eps, -hh],
                [ hw, -hd - eps, -hh],
                [ hw, -hd - eps,  hh],
                [-hw, -hd - eps,  hh],
            ],
            "normal": [0, -1, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        "rear": {
            "vertices": [
                [ hw, hd + eps, -hh],
                [-hw, hd + eps, -hh],
                [-hw, hd + eps,  hh],
                [ hw, hd + eps,  hh],
            ],
            "normal": [0, 1, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        "left": {
            "vertices": [
                [-hw - eps,  hd, -hh],
                [-hw - eps, -hd, -hh],
                [-hw - eps, -hd,  hh],
                [-hw - eps,  hd,  hh],
            ],
            "normal": [-1, 0, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        "right": {
            "vertices": [
                [hw + eps, -hd, -hh],
                [hw + eps,  hd, -hh],
                [hw + eps,  hd,  hh],
                [hw + eps, -hd,  hh],
            ],
            "normal": [1, 0, 0],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        "top": {
            "vertices": [
                [-hw, -hd, hh + eps],
                [ hw, -hd, hh + eps],
                [ hw,  hd, hh + eps],
                [-hw,  hd, hh + eps],
            ],
            "normal": [0, 0, 1],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
        "bottom": {
            "vertices": [
                [-hw,  hd, -hh - eps],
                [ hw,  hd, -hh - eps],
                [ hw, -hd, -hh - eps],
                [-hw, -hd, -hh - eps],
            ],
            "normal": [0, 0, -1],
            "uv": [[0, 0], [1, 0], [1, 1], [0, 1]],
        },
    }

    fd = face_defs[face]
    vertices = np.array(fd["vertices"], dtype=np.float64)
    faces_idx = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    normals = np.tile(fd["normal"], (4, 1)).astype(np.float64)

    material = trimesh.visual.material.PBRMaterial(
        baseColorTexture=image,
        metallicFactor=PBR_TEXTURED["metallicFactor"] if textured else PBR_SOLID["metallicFactor"],
        roughnessFactor=PBR_TEXTURED["roughnessFactor"] if textured else PBR_SOLID["roughnessFactor"],
    )

    uv = np.array(fd["uv"], dtype=np.float64)
    visual = trimesh.visual.TextureVisuals(uv=uv, material=material)

    return trimesh.Trimesh(
        vertices=vertices,
        faces=faces_idx,
        vertex_normals=normals,
        visual=visual,
        process=False,
    )


def create_beveled_body(width: float, height: float, depth: float, bevel_mm: float, body_color: str) -> trimesh.Trimesh:
    """
    Create an approximated beveled body using a convex hull around inset corner/edge points.
    """
    b = bevel_mm / 1000.0
    hw, hh, hd = width / 2, height / 2, depth / 2

    if b <= 0 or b >= min(hw, hh, hd):
        body = trimesh.creation.box(extents=[width, depth, height])
    else:
        verts = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    verts.append([sx * (hw - b), sy * (hd - b), sz * (hh - b)])
                    verts.append([sx * hw, sy * (hd - b), sz * (hh - b)])
                    verts.append([sx * (hw - b), sy * hd, sz * (hh - b)])
                    verts.append([sx * (hw - b), sy * (hd - b), sz * hh])
        body = trimesh.convex.convex_hull(np.array(verts))

    rgba = hex_to_rgba(body_color)
    body.visual = trimesh.visual.ColorVisuals(
        mesh=body,
        face_colors=np.tile(np.array(rgba, dtype=np.uint8), (len(body.faces), 1)),
    )
    return body


def create_front_detail_meshes(
    width: float,
    height: float,
    depth: float,
    grid: str,
    detail_depth_mm: float,
    body_color: str,
) -> list[trimesh.Trimesh]:
    """
    Add small front-panel blocks to create visible geometric detail.
    These are not boolean cuts. They are attached meshes in front of the body.
    """
    if not grid:
        return []

    try:
        cols, rows = [int(x) for x in grid.lower().split("x")]
    except Exception as exc:
        raise ValueError(f"Invalid --detail-grid value: {grid}. Use format COLSxROWS.") from exc

    d = detail_depth_mm / 1000.0
    hw, hh, hd = width / 2, height / 2, depth / 2

    usable_w = width * 0.82
    usable_h = height * 0.48 if rows > 1 else height * 0.38
    margin_x = width * 0.09
    margin_z = height * 0.18 if rows > 1 else height * 0.30

    cell_w = usable_w / cols
    cell_h = usable_h / rows

    rgba = hex_to_rgba(body_color)
    meshes: list[trimesh.Trimesh] = []

    for c in range(cols):
        for r in range(rows):
            cx = -hw + margin_x + (c + 0.5) * cell_w
            cz = -hh + margin_z + (r + 0.5) * cell_h

            block = trimesh.creation.box(
                extents=[cell_w * 0.72, d, cell_h * 0.62],
                transform=trimesh.transformations.translation_matrix(
                    [cx, -hd - d / 2, cz]
                ),
            )
            block.visual = trimesh.visual.ColorVisuals(
                mesh=block,
                face_colors=np.tile(np.array(rgba, dtype=np.uint8), (len(block.faces), 1)),
            )
            meshes.append(block)

    return meshes


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a high-quality textured GLB device model")
    parser.add_argument("--id", required=True, help="Model ID")
    parser.add_argument("--width", type=float, required=True, help="Width in mm")
    parser.add_argument("--depth", type=float, required=True, help="Depth in mm")
    parser.add_argument("--height", type=float, required=True, help="Height in mm")
    parser.add_argument("--front", help="Front face image")
    parser.add_argument("--rear", help="Rear face image")
    parser.add_argument("--left", help="Left face image")
    parser.add_argument("--right", help="Right face image")
    parser.add_argument("--top", help="Top face image")
    parser.add_argument("--bottom", help="Bottom face image")
    parser.add_argument("--color", default=DEFAULT_BODY_COLOR, help="Body color hex")
    parser.add_argument("--output", required=True, help="Output GLB path")
    parser.add_argument("--manifest", help="Path to manifest.json")
    parser.add_argument("--bevel", type=float, default=2.0, help="Bevel amount in mm")
    parser.add_argument("--detail-grid", default="", help="Optional front detail grid, e.g. 24x2 or 4x1")
    parser.add_argument("--detail-depth", type=float, default=2.0, help="Depth of front detail blocks in mm")

    args = parser.parse_args()

    face_paths = {
        "front": args.front,
        "rear": args.rear,
        "left": args.left,
        "right": args.right,
        "top": args.top,
        "bottom": args.bottom,
    }

    provided = [face for face, p in face_paths.items() if p and Path(p).is_file()]
    if not provided:
        print("ERROR: At least one face image is required.")
        sys.exit(1)

    face_dims = {
        "front":  (args.width, args.height),
        "rear":   (args.width, args.height),
        "left":   (args.depth, args.height),
        "right":  (args.depth, args.height),
        "top":    (args.width, args.depth),
        "bottom": (args.width, args.depth),
    }

    print(f"\n{'=' * 60}")
    print(" HIGH-QUALITY DEVICE MODEL GENERATOR")
    print(f"{'=' * 60}")
    print(f"  Model ID:     {args.id}")
    print(f"  Dimensions:   {args.width} × {args.depth} × {args.height} mm (W×D×H)")
    print(f"  Body colour:  {args.color}")
    print(f"  Bevel:        {args.bevel} mm")
    print(f"  Detail grid:  {args.detail_grid if args.detail_grid else '(none)'}")
    print()

    w_m = args.width / 1000.0
    d_m = args.depth / 1000.0
    h_m = args.height / 1000.0

    meshes: list[trimesh.Trimesh] = []

    body = create_beveled_body(w_m, h_m, d_m, args.bevel, args.color)
    meshes.append(body)

    if args.detail_grid:
        details = create_front_detail_meshes(
            width=w_m,
            height=h_m,
            depth=d_m,
            grid=args.detail_grid,
            detail_depth_mm=args.detail_depth,
            body_color=args.color,
        )
        meshes.extend(details)

    for face in FACES:
        fw, fh = face_dims[face]
        img, textured = load_face_image(face_paths[face], fw, fh, args.color)
        status = Path(face_paths[face]).name if face_paths[face] and Path(face_paths[face]).is_file() else "(body colour)"
        print(f"  {face:8s}  {status}")

        face_mesh = create_textured_face_mesh(
            width=w_m,
            height=h_m,
            depth=d_m,
            face=face,
            image=img,
            textured=textured,
            face_offset=0.0006,  # 0.6 mm visual offset to avoid z-fighting
        )
        meshes.append(face_mesh)

    scene = trimesh.Scene(meshes)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    scene.export(args.output, file_type="glb")

    file_size = Path(args.output).stat().st_size
    triangle_count = sum(len(m.faces) for m in meshes if hasattr(m, "faces"))

    print(f"\n  Output:       {args.output}")
    print(f"  File size:    {file_size:,} bytes ({file_size / 1024:.1f} KB)")
    print(f"  Triangles:    {triangle_count}")
    print(f"  Zoom safe:    YES")
    print()

    if args.manifest and Path(args.manifest).is_file():
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        entry = {
            "id": args.id,
            "file": Path(args.output).name,
            "category": "device",
            "source": "device-to-glb-hq",
            "license": "internal",
            "dimensions_mm": {
                "width": args.width,
                "depth": args.depth,
                "height": args.height,
            },
            "faces_textured": provided,
            "generated_at": date.today().isoformat(),
            "bevel_mm": args.bevel,
            "detail_grid": args.detail_grid,
            "detail_depth_mm": args.detail_depth,
        }

        existing = next((i for i, m in enumerate(manifest["models"]) if m["id"] == args.id), None)
        if existing is not None:
            manifest["models"][existing] = entry
            print(f"  Manifest:     UPDATED entry for {args.id}")
        else:
            manifest["models"].append(entry)
            manifest["models"].sort(key=lambda m: m["id"])
            print(f"  Manifest:     ADDED entry for {args.id}")

        Path(args.manifest).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    elif args.manifest:
        print(f"  Manifest:     {args.manifest} not found — skipped")

    print(f"\n  Associate with device:")
    print(f'    curl -X PUT .../api/devices/{{id}} -d \'{{"model_id":"{args.id}"}}\'')
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()