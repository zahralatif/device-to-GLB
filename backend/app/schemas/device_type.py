from pydantic import BaseModel


class DeviceTypeBase(BaseModel):
    name: str


class DeviceTypeCreate(DeviceTypeBase):
    pass


class DeviceTypeResponse(DeviceTypeBase):
    id: int

    class Config:
        from_attributes = True