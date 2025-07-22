from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

try:
    # Create engine - connections will be handled at runtime
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG,
        pool_recycle=300,
        pool_timeout=60
    )
    print(f"✅ Database engine created: {settings.DATABASE_URL[:50]}...")
except Exception as e:
    print(f"❌ Database engine creation failed: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()