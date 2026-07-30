from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.vendor import (
    get_vendors,
    get_vendor,
    create_vendor,
    delete_vendor,
)
from app.db.dependencies import get_db
from app.schemas.vendor import VendorCreate, VendorResponse

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"],
)


@router.get("/", response_model=list[VendorResponse])
def read_vendors(db: Session = Depends(get_db)):
    return get_vendors(db)


@router.get("/{vendor_id}", response_model=VendorResponse)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = get_vendor(db, vendor_id)

    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return vendor


@router.post("/", response_model=VendorResponse, status_code=201)
def create_new_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
):
    return create_vendor(db, vendor)


@router.delete("/{vendor_id}")
def remove_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
):
    vendor = delete_vendor(db, vendor_id)

    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return {"message": "Vendor deleted"}