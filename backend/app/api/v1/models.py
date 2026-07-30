from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import device_model as crud
from app.db.dependencies import get_db
from app.schemas.device_model import (
    DeviceModelCreate,
    DeviceModelResponse,
)

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


@router.post(
    "/",
    response_model=DeviceModelResponse,
)
def create_model(
    model: DeviceModelCreate,
    db: Session = Depends(get_db),
):
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