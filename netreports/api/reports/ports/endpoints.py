"""API endpoints for ports report."""
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from netreports.api.reports.ports import COLLECTION_NAME, models
from netreports.core.db.mongodb import get_database
from netreports.core.utils import find_parameters
from netreports.core.crud.base import get_documents, insert_many_documents


router = APIRouter(prefix="/ports", tags=["ports"])


@router.get("/")
async def get_all_ports_data(
    find_params: dict = Depends(find_parameters), db_client: MongoClient = Depends(get_database)
):
    """Fetch all ports report data with basic filtering for skip/limit."""
    count, documents = await get_documents(db_client, COLLECTION_NAME, return_model=models.PortsBody, **find_params)
    return {"count": count, "results": documents}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ports_bulk(payload: List[models.PortsBody], db_client: MongoClient = Depends(get_database)):
    """Bulk create ports data passed in."""
    await insert_many_documents(db_client, COLLECTION_NAME, payload)
    return JSONResponse(content={"message": "Ports report data created."}, status_code=status.HTTP_201_CREATED)
