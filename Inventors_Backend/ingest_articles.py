import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Article
from datetime import datetime

NEWS_API_KEY = "dda2130885524084986ebeee0b44e1b2"
API_URL = f"https://newsapi.org/v2/everything?q=technology&apiKey={NEWS_API_KEY}"

def fetch_articles():
    response = requests.get(API_URL)
    data = response.json()
    return data.get("articles", [])

def store_articles():
    db: Session = SessionLocal()
    for item in fetch_articles():
        article = Article(
            title=item["title"],
            url=item["url"],
            source=item.get("source", {}).get("name", ""),
            summary=item.get("description", ""),
            tags=["tech"],  # simple default tag
            published_date=datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        )
        try:
            db.add(article)
            db.commit()
        except Exception as e:
            db.rollback()  # in case of duplicates or errors
            print(f"Skipped: {article.title} ({e})")
    db.close()

if __name__ == "__main__":
    store_articles()
