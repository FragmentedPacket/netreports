"""Stuff."""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient

from netreports.db.mongodb import get_database
from netreports.core.utils import find_parameters
from netreports.crud.base import get_documents, insert_many_documents


router = APIRouter(prefix="/ports", tags=["ports"])


class PortsBody(BaseModel):
    device: str
    ports_total: int
    ports_up: int
    ports_down: int
    ports_shutdown: int
    domain: Optional[str] = None


@router.get("/")
async def get_all_ports_data(
    find_params: dict = Depends(find_parameters), db_client: MongoClient = Depends(get_database)
):
    count, documents = await get_documents(db_client, "ports", return_model=PortsBody, **find_params)
    return {"count": count, "results": documents}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ports_bulk(payload: List[PortsBody], db_client: MongoClient = Depends(get_database)):
    await insert_many_documents(db_client, "ports", payload)
    return JSONResponse(content={"message": "Ports report data created."}, status_code=status.HTTP_201_CREATED)
