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
    "Rack",
]


def seed_device_types(db: Session):
    for name in DEFAULT_DEVICE_TYPES:
        exists = (
            db.query(DeviceType)
            .filter(DeviceType.name == name)
            .first()
        )

        if not exists:
            db.add(DeviceType(name=name))

    db.commit()