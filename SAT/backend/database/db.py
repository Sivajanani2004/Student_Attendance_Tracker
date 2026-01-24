from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")

UPLOAD_DIR = "uploads"

SessionLocal = sessionmaker(bind = engine,autoflush = False,autocommit = False)