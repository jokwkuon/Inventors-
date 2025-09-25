
from database import engine, Base
import logging

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully!")
    print("Tables created successfully!")
