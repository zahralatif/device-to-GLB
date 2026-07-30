from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.device_type import DeviceType
from app.models.device_model import DeviceModel


def get_catalog_tree(db: Session):
    vendors = db.query(Vendor).order_by(Vendor.name).all()

    result = []

    for vendor in vendors:
        vendor_node = {
            "id": vendor.id,
            "name": vendor.name,
            "device_types": [],
        }

        device_types = (
            db.query(DeviceType)
            .join(
                DeviceModel,
                DeviceModel.device_type_id == DeviceType.id,
            )
            .filter(DeviceModel.vendor_id == vendor.id)
            .distinct()
            .all()
        )

        for device_type in device_types:
            models = (
                db.query(DeviceModel)
                .filter(
                    DeviceModel.vendor_id == vendor.id,
                    DeviceModel.device_type_id == device_type.id,
                )
                .order_by(DeviceModel.model_id)
                .all()
            )

            vendor_node["device_types"].append(
                {
                    "id": device_type.id,
                    "name": device_type.name,
                    "models": [
                        {
                            "id": model.id,
                            "model_id": model.model_id,
                            "model_series": model.model_series,
                        }
                        for model in models
                    ],
                }
            )

        result.append(vendor_node)

    return result