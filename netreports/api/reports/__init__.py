"""Base for all report routers, etc."""
from fastapi import APIRouter

from netreports.api.reports.ports import endpoints as ports_endpoints

router = APIRouter(prefix="/api/reports")

router.include_router(ports_endpoints.router)
