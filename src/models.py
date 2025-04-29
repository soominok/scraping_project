from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, DateTime

Base = declarative_base()

class Review(Base):
    __tablename__ = "naver_reviews"

    review_id = Column(String(50), primary_key=True, nullable = False)
    user_id = Column(String(50), nullable = False)
    nicekname = Column(String(50))
    contents = Column(text)
    rating = Column(String(50))
    update_at = Column(DateTime)
    naver_place_id = Column(String(50), nullable = False)
    naver_place_name = Column(STring(100), nullable = False)
    
    