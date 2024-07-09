# pylint: disable=C0116
import json
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schema.search import SearchResponse
from app.service.abn_service import download_all_and_ingest, ingest_one

router = APIRouter()

@router.get("/download_and_ingest", response_model={})
async def download_and_ingest():
    try:
        download_all_and_ingest()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/ingest_one", response_model={})
async def ingest():
    try:
        ingest_one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
