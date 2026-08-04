from pydantic import BaseModel
from typing import Optional


class DeviceModelBase(BaseModel):
    model_id: str
    model_series: str

    rack_units: Optional[int] = None
    part_number: Optional[str] = None

    body_colour: Optional[str] = None

    front_image: Optional[str] = None
    rear_image: Optional[str] = None
    left_image: Optional[str] = None
    right_image: Optional[str] = None
    top_image: Optional[str] = None
    bottom_image: Optional[str] = None


class DeviceModelCreate(DeviceModelBase):
    device_type_id: int
    vendor_id: int


class DeviceModelUpdate(BaseModel):
    model_series: Optional[str] = None

    rack_units: Optional[int] = None
    part_number: Optional[str] = None

    body_colour: Optional[str] = None

    device_type_id: Optional[int] = None
    vendor_id: Optional[int] = None


class DeviceModelResponse(DeviceModelBase):
    id: int

    device_type_id: int
    vendor_id: int
    status: str

    glb_path: Optional[str] = None

    class Config:
        from_attributes = True