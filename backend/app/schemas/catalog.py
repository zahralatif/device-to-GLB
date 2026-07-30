from pydantic import BaseModel

from app.schemas.vendor import VendorResponse
from app.schemas.device_type import DeviceTypeResponse
from app.schemas.device_model import DeviceModelResponse


class CatalogTreeResponse(BaseModel):
    vendors: list[VendorResponse]
    device_types: list[DeviceTypeResponse]
    models: list[DeviceModelResponse]