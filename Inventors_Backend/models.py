from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from database import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    source = Column(String)
    published_date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    tags = Column(ARRAY(String))
