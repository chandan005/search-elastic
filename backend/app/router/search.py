import json
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schema.search import SearchResponse
from app.service.search_service import get_search

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def qa_endpoint(questions_file: UploadFile = File(...), document_file: UploadFile = File(...)):
    try:
        searches = []
        return SearchResponse(searches=searches)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
