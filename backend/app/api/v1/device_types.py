from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.device_type import (
    DeviceTypeCreate,
    DeviceTypeResponse,
)
from app.crud import device_type

router = APIRouter(
    prefix="/device-types",
    tags=["Device Types"],
)


@router.get("/", response_model=list[DeviceTypeResponse])
def get_device_types(db: Session = Depends(get_db)):
    return device_type.get_all(db)


@router.get("/{device_type_id}", response_model=DeviceTypeResponse)
def get_device_type(
    device_type_id: int,
    db: Session = Depends(get_db),
):
    db_device_type = device_type.get_by_id(
        db,
        device_type_id,
    )

    if not db_device_type:
        raise HTTPException(
            status_code=404,
            detail="Device type not found",
        )

    return db_device_type


@router.post("/", response_model=DeviceTypeResponse)
def create_device_type(
    device: DeviceTypeCreate,
    db: Session = Depends(get_db),
):
    return device_type.create(db, device)


@router.delete("/{device_type_id}")
def delete_device_type(
    device_type_id: int,
    db: Session = Depends(get_db),
):
    db_device_type = device_type.delete(
        db,
        device_type_id,
    )

    if not db_device_type:
        raise HTTPException(
            status_code=404,
            detail="Device type not found",
        )

    return {"message": "Device type deleted"}