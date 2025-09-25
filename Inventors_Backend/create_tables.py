from database import engine, Base
from models import Article

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
