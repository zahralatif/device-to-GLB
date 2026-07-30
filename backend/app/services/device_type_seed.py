from sqlalchemy.orm import Session

from app.models.device_type import DeviceType

DEFAULT_DEVICE_TYPES = [
    "Server",
    "Switch",
    "Router",
    "Firewall",
    "Storage",
    "UPS",
    "PDU",
]


def seed_device_types(db: Session):
    existing = {
        item.name
        for item in db.query(DeviceType).all()
    }

    for name in DEFAULT_DEVICE_TYPES:
        if name not in existing:
            db.add(DeviceType(name=name))

    db.commit()
    