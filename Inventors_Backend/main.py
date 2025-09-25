from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Article
from schemas import ArticleCreate, ArticleResponse
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Jok, please finish this app"}

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/", response_model=ArticleResponse)
def add_article(article: ArticleCreate, db: Session = Depends(get_db)):
    new_article = Article(
        title=article.title,
        url=article.url,
        source=article.source,
        summary=article.summary,
        tags=article.tags,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.get("/articles/", response_model=List[ArticleResponse])
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()
