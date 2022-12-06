from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

if settings.database_url is not None:
    url = settings.database_url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DB_URL = url
else: 
    SQLALCHEMY_DB_URL = f"{settings.database}://{settings.db_user}:{settings.db_password}" \
                        f"@{settings.host}:{settings.port}/{settings.db_name}"
    
    engine = create_engine(SQLALCHEMY_DB_URL)
    SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()