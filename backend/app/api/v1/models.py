from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app.crud import device_model as crud
from app.models.device_model import DeviceModel
from app.db.dependencies import get_db
from app.schemas.device_model import (
    DeviceModelCreate,
    DeviceModelResponse,
)
from app.services.model_validation_service import (
    validate_model_id,
)
from app.services.upload_service import save_upload
from app.services.prepare_image_service import prepare_image
from app.services.glb_generation_service import generate_glb

router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


@router.get(
    "/",
    response_model=list[DeviceModelResponse],
)
def get_models(db: Session = Depends(get_db)):
    return crud.get_all(db)


@router.get(
    "/{model_id}",
    response_model=DeviceModelResponse,
)
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
):
    model = crud.get_by_id(db, model_id)

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    return model


@router.post("/", response_model=DeviceModelResponse)
def create_model(
    model: DeviceModelCreate,
    db: Session = Depends(get_db),
):
    if not validate_model_id(model.model_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid model_id format",
        )

    return crud.create(db, model)


@router.delete("/{model_id}")
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
):
    model = crud.delete(db, model_id)

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    return {"message": "Model deleted"}

@router.post("/{model_id}/upload/{face}")
def upload_model_face(
    model_id: str,
    face: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    model = (
        db.query(DeviceModel)
        .filter(DeviceModel.model_id == model_id)
        .first()
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    path = save_upload(
        model.model_id,
        face,
        file,
    )

    prepared_path = prepare_image(
        model.model_id,
        face,
        path,
    )

    crud.update_face_image(
        db,
        model,
        face,
        path,
    )

    return {
    "original": path,
    "prepared": prepared_path,
    }

@router.post("/{model_id}/generate")
def generate_model_glb(
    model_id: str,
    db: Session = Depends(get_db),
):
    model = crud.get_by_model_id(
        db,
        model_id,
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    required_faces = [
        model.front_image,
        model.rear_image,
        model.left_image,
        model.right_image,
        model.top_image,
        model.bottom_image,
    ]

    if not any(required_faces):
        raise HTTPException(
            status_code=400,
            detail="No uploaded images found",
        )

    glb_path = generate_glb(
        model.model_id,
    )

    crud.update_glb_path(
        db,
        model,
        glb_path,
    )

    return {
        "model_id": model.model_id,
        "glb": glb_path,
        "status": "generated",
    }

@router.get("/{model_id}/gallery")
def get_gallery(
    model_id: str,
    db: Session = Depends(get_db),
):
    model = crud.get_by_model_id(
        db,
        model_id,
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    return {
        "model_id": model.model_id,
        "images": {
            "front": model.front_image,
            "rear": model.rear_image,
            "left": model.left_image,
            "right": model.right_image,
            "top": model.top_image,
            "bottom": model.bottom_image,
        },
        "glb": model.glb_path,
    }

@router.get("/{model_id}/preview")
def preview_model(
    model_id: str,
    db: Session = Depends(get_db),
):
    model = crud.get_by_model_id(
        db,
        model_id,
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    if not model.glb_path:
        raise HTTPException(
            status_code=400,
            detail="GLB has not been generated yet",
        )

    return {
        "model_id": model.model_id,
        "glb": model.glb_path,
    }