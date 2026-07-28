from pydantic import BaseModel


class VendorBase(BaseModel):
    name: str


class VendorCreate(VendorBase):
    pass


class VendorResponse(VendorBase):
    id: int

    class Config:
        from_attributes = True