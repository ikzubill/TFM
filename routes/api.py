from fastapi import APIRouter
from endpoints import udemy
from endpoints import healthcheck

router = APIRouter()

router.include_router(udemy.router, tags=["Busqueda en Udemy"])
router.include_router(healthcheck.router, tags=["Health Check"])
