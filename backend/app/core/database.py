from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
from app.models.base import Base
from app.models.relationships import setup_relationships

load_dotenv()

# Get database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up all relationships
setup_relationships()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()