from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str = Field(..., max_length=512)
    url: HttpUrl
    source: Optional[str] = ""
    summary: Optional[str] = ""
    tags: List[str] = []

class ArticleResponse(BaseModel):
    id: int
    title: str
    url: HttpUrl
    source: Optional[str]
    summary: Optional[str]
    tags: List[str]
    published_date: Optional[datetime]

    class Config:
        orm_mode = True
