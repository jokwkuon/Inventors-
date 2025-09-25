from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Article

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/")
def add_article(title: str, url: str, source: str, summary: str = "", tags: list[str] = [], db: Session = Depends(get_db)):
    new_article = Article(title=title, url=url, source=source, summary=summary, tags=tags)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.get("/articles/")
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()
