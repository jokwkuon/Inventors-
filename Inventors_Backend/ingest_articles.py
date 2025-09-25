"""
Ingest articles from NewsAPI into the database.

Usage:
    python ingest_articles.py                    # ingests all returned articles
    python ingest_articles.py --limit 5         # ingest only first 5 results
    python ingest_articles.py --query AI        # ingest articles matching query "AI"
"""

import os
import argparse
import requests
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import SessionLocal
from models import Article
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from .env
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY is required in .env")

API_URL = "https://newsapi.org/v2/everything"

def fetch_articles(q: str = "technology", page_size: int = 100):
    """Fetch articles from NewsAPI."""
    params = {
        "q": q,
        "pageSize": page_size,
        "language": "en"
    }
    headers = {"X-Api-Key": NEWS_API_KEY}
    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("articles", [])
    except requests.RequestException as e:
        logger.error(f"Network/API error while fetching articles: {e}")
        return []

def parse_published_at(s: str):
    """Parse NewsAPI date strings into datetime."""
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    logger.warning("Unable to parse publishedAt: %s", s)
    return None

def store_articles(query: str = "technology", limit: int = None, page_size: int = 100):
    """Fetch and store articles in the database."""
    db: Session = SessionLocal()
    ingested, skipped = 0, 0
    try:
        articles = fetch_articles(q=query, page_size=page_size)
        if limit:
            articles = articles[:limit]

        for item in articles:
            url = item.get("url")
            if not url:
                logger.debug("Skipping article without URL: %s", item.get("title"))
                skipped += 1
                continue

            # Deduplication check
            if db.query(Article).filter(Article.url == url).first():
                logger.info("Skipping existing article: %s", url)
                skipped += 1
                continue

            published_date = parse_published_at(item.get("publishedAt"))

            article = Article(
                title=item.get("title") or "Untitled",
                url=url,
                source=item.get("source", {}).get("name", ""),
                summary=item.get("description") or "",
                tags=item.get("tags") or ["tech"],
                published_date=published_date
            )
            try:
                db.add(article)
                db.commit()
                ingested += 1
            except IntegrityError as e:
                db.rollback()
                logger.warning("IntegrityError inserting %s: %s", url, e)
                skipped += 1
            except SQLAlchemyError as e:
                db.rollback()
                logger.error("DB error inserting %s: %s", url, e)
                skipped += 1
    finally:
        db.close()

    logger.info("Ingest complete — ingested=%d skipped=%d", ingested, skipped)
    return ingested, skipped

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest articles from NewsAPI into the DB.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of articles ingested")
    parser.add_argument("--query", type=str, default="technology", help="Search query for articles")
    parser.add_argument("--page-size", type=int, default=100, help="Number of articles per API request")
    args = parser.parse_args()

    store_articles(query=args.query, limit=args.limit, page_size=args.page_size)
