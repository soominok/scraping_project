from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScrapingJob(Base):
    __tablename__ = 'scraping_jobs'
    id = Column(Integer, primary_key=True)
    place_id = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_onupdate='CURRENT_TIMESTAMP')

class PlaceData(Base):
    __tablename__ = 'place_data'
    place_id = Column(String(255), primary_key=True)
    source = Column(String(50), primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    phone_number = Column(String(20))
    category = Column(String(100))
    latitude = Column(Float(precision=7))
    longitude = Column(Float(precision=7))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_onupdate='CURRENT_TIMESTAMP')

class ReviewData(Base):
    __tablename__ = 'review_data'
    id = Column(Integer, primary_key=True)
    place_id = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    review_id = Column(String(255), nullable=False)
    author = Column(String(255))
    rating = Column(Float)
    content = Column(Text)
    created_at = Column(DateTime)
