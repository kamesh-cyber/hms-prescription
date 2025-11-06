from fastapi import APIRouter
from app.routes.prescription import router as prescription_router

router = APIRouter()

# Include all route modules
router.include_router(prescription_router)

__all__ = ["router"]

