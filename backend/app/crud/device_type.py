from sqlalchemy.orm import Session

from app.models.device_type import DeviceType
from app.schemas.device_type import DeviceTypeCreate


def get_all(db: Session):
    return db.query(DeviceType).all()


def get_by_id(db: Session, device_type_id: int):
    return (
        db.query(DeviceType)
        .filter(DeviceType.id == device_type_id)
        .first()
    )


def create(db: Session, device_type: DeviceTypeCreate):
    db_device_type = DeviceType(**device_type.model_dump())

    db.add(db_device_type)
    db.commit()
    db.refresh(db_device_type)

    return db_device_type


def delete(db: Session, device_type_id: int):
    db_device_type = get_by_id(db, device_type_id)

    if db_device_type:
        db.delete(db_device_type)
        db.commit()

    return db_device_type