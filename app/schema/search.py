from typing import List
from pydantic import BaseModel

class Search(BaseModel):
    question: str
    answer: str

class SearchResponse(BaseModel):
    searches: List[Search]
