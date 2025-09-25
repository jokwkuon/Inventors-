from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str
    url: str
    source: str
    summary: Optional[str] = ""
    tags: List[str] = []

class ArticleResponse(ArticleCreate):
    id: int
    published_date: Optional[datetime] = None

    class Config:
        orm_mode = True
