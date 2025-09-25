from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Article
from schemas import ArticleCreate, ArticleResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Inventors Backend")

# CORS — allow your frontend origin(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # update to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in development if missing. For production, use migrations (alembic).
if os.getenv("APP_ENV", "development") == "development":
    Base.metadata.create_all(bind=engine)
    logger.info("DB tables ensured (development mode)")

@app.get("/")
def read_root():
    return {"message": "🚀 Inventors Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def add_article(article: ArticleCreate, db: Session = Depends(get_db)):
    # check duplicate
    existing = db.query(Article).filter(Article.url == str(article.url)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Article already exists")

    new_article = Article(
        title=article.title,
        url=str(article.url),
        source=article.source,
        summary=article.summary,
        tags=article.tags,
    )
    try:
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
    except IntegrityError as e:
        db.rollback()
        logger.error("IntegrityError saving article: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not save article")
    return new_article

@app.get("/articles/", response_model=List[ArticleResponse])
def get_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Article).offset(skip).limit(limit).all()
