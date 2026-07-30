from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate


def get_vendors(db: Session):
    return db.query(Vendor).order_by(Vendor.name).all()


def get_vendor(db: Session, vendor_id: int):
    return (
        db.query(Vendor)
        .filter(Vendor.id == vendor_id)
        .first()
    )


def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(**vendor.model_dump())

    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)

    return db_vendor


def delete_vendor(db: Session, vendor_id: int):
    vendor = get_vendor(db, vendor_id)

    if vendor is None:
        return None

    db.delete(vendor)
    db.commit()

    return vendor