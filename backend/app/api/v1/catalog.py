from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.catalog_service import get_catalog_tree

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@router.get("/tree")
def catalog_tree(
    db: Session = Depends(get_db),
):
    return get_catalog_tree(db)