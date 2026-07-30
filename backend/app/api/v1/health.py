from fastapi import APIRouter

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}