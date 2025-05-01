from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum



class BaseModel(object):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

Base = declarative_base(cls=BaseModel)

class ScrapeJob(Base):
    __tablename__ = "scraping_jobs"
    id = Column(Integer, primary_key = True, autoincrement = True)
    task_id = Column(String(36), unique = True)
    status = Column(Enum('IN_PROGRESS', 'SUCCESS', 'FAILED'))
    platform = Column(String(10))
    place_name = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    error_log = Column(Text)
    
    
class NaverInfo(Base):
    __tablename__ = "naver_info"
    id = Column(Integer, primary_key = True, autoincrement = True)
    place_id = Column(String(50), nullable = False, unique = True)
    place_name = Column(String(100), nullable = False)
    address = Column(String(300))
    tel = Column(String(50))
    platform = Column(String(10))
    task_id = Column(String(50))
    
class KakaoInfo(Base):
    __tablename__ = "kakao_info"
    id = Column(Integer, primary_key = True, autoincrement = True)
    place_id = Column(String(50), nullable = False, unique = True)
    place_name = Column(String(100), nullable = False)
    address = Column(String(300))
    tel = Column(String(50))
    platform = Column(String(10))
    task_id = Column(String(50))


class NaverReview(Base):
    __tablename__ = "naver_reviews"
    id = Column(Integer, primary_key = True, autoincrement = True)
    review_id = Column(String(50), nullable = False, unique = True)
    user_id = Column(String(50), nullable = False)
    nickname = Column(String(50))
    contents = Column(Text)
    rating = Column(String(50))
    updated_at = Column(DateTime)
    place_id = Column(String(50), nullable = False)
    place_name = Column(String(100), nullable = False)
    updated_at = Column(DateTime)
    platform = Column(String(100), nullable = False)
    task_id = Column(String(50))


class KakaoReview(Base):
    __tablename__ = "kakao_reviews"

    id = Column(Integer, primary_key = True, autoincrement = True)
    review_id = Column(String(50), nullable = False, unique = True)
    user_id = Column(String(50), nullable = False)
    nickname = Column(String(50))
    contents = Column(Text)
    rating = Column(String(50))
    updated_at = Column(DateTime)
    place_id = Column(String(50), nullable = False)
    place_name = Column(String(100), nullable = False)
    updated_at = Column(DateTime)
    platform = Column(String(100), nullable = False)
    task_id = Column(String(50))
    