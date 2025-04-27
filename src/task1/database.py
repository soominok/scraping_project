from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

class PlaceInfo(Base):
    __tablename__ = 'place_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    phone_number = Column(String(50))
    naver_url = Column(Text)
    kakao_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PlaceInfo(name='{self.name}', address='{self.address}')>"

class ScrapingJob(Base):
    __tablename__ = 'scraping_jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), default='InProgress')
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    success = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ScrapingJob(job_id='{self.job_id}', status='{self.status}')>"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()