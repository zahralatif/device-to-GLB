from sqlalchemy.orm import Session

from app.models.device_model import DeviceModel
from app.schemas.device_model import DeviceModelCreate


def get_all(db: Session):
    return db.query(DeviceModel).all()


def get_by_id(db: Session, model_id: int):
    return (
        db.query(DeviceModel)
        .filter(DeviceModel.id == model_id)
        .first()
    )


def create(db: Session, model: DeviceModelCreate):
    db_model = DeviceModel(**model.model_dump())

    db.add(db_model)
    db.commit()
    db.refresh(db_model)

    return db_model


def delete(db: Session, model_id: int):
    db_model = get_by_id(db, model_id)

    if db_model:
        db.delete(db_model)
        db.commit()

    return db_model
    
def update_face_image(
    db: Session,
    model: DeviceModel,
    face: str,
    path: str,
):
    setattr(model, f"{face}_image", path)

    db.commit()
    db.refresh(model)

    return model