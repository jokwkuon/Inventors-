from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from database import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    url = Column(String(1024), nullable=False, unique=True, index=True)
    source = Column(String(256))
    published_date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    tags = Column(JSON)  # JSON is portable across DBs and works well for simple tag lists

    def __repr__(self):
        return f"<Article id={self.id} title={self.title!r}>"
