# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# 환경변수에서 DATABASE_URL을 읽어옵니다
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/reviews_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class KCDInfo(Base):
    

class NaverInfo(Base):
    __tablename__ = 'kakao_reviews'

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(50))
    author = Column(String(255))
    content = Column(Text)
    rating = Column(Integer)
    visit_date = Column(Date)
    collected_at = Column(DateTime, default=datetime.datetime.utcnow)

class NaverReview(Base):
    __tablename__ = 'kakao_reviews'

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(50))
    author = Column(String(255))
    content = Column(Text)
    rating = Column(Integer)
    visit_date = Column(Date)
    collected_at = Column(DateTime, default=datetime.datetime.utcnow)



class KakaoReview(Base):
    __tablename__ = 'kakao_reviews'

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(50))
    author = Column(String(255))
    content = Column(Text)
    rating = Column(Integer)
    visit_date = Column(Date)
    collected_at = Column(DateTime, default=datetime.datetime.utcnow)



def save_reviews_to_db(reviews: list, place_id: str):
    session = SessionLocal()
    try:
        for r in reviews:
            review = KakaoReview(
                place_id=place_id,
                author=r['author'],
                content=r['content'],
                rating=r['rating'],
                visit_date=r['visit_date'] if r['visit_date'] else None
            )
            session.add(review)
        session.commit()
    except Exception as e:
        print("DB Save Error:", e)
        session.rollback()
    finally:
        session.close()