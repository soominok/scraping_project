from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.db.models import Base, ScrapeJob, NaverInfo, KakaoInfo, NaverReview, KakaoReview
from src.utils.config import DB_CONFIG
#DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_DATABASE


db_url = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@{DB_CONFIG['host']}/"
            f"{DB_CONFIG['database']}?charset=utf8"
)

engine = create_engine(db_url, echo = True, pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
# con = engine.connect()

def init_db():
    Base.metadata.create_all(bind = engine)
    print("데이터베이스 테이블 생성 완료")
    

def log_job_status(task_id, status, platform, place_name, error_log = None):
    db = SessionLocal()
    try:
        job = ScrapeJob(
            task_id = task_id,
            status = status,
            platform = platform,
            place_name = place_name,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow(),
            error_log = error_log
        )
        db.add(job)
        db.commit()
    finally:
        db.close()
        
def update_job_status(task_id, status, error_log = None):
    db = SessionLocal()
    try:
        job = db.query(ScrapeJob).filter(ScrapeJob.task_id == task_id).first()
        if job:
            job.status = status
            job.update_at = datetime.utcnow()
            if error_log:
                job.error_log = error_log
            db.commit()
            
    finally:
        db.close()
        
        
def save_place_info(place_id, place_name, address, tel, platform, task_id):
    db = SessionLocal()
    try:
        if platform == 'naver':
            place_info = NaverInfo(
                place_id = place_id,
                place_name = place_name,
                address = address,
                tel = tel,
                platform = platform,
                task_id = task_id
            )
            
        if platform == 'kakao':
            place_info = KakaoInfo(
                place_id = place_id,
                place_name = place_name,
                address = address,
                tel = tel,
                platform = platform,
                task_id = task_id
            )
            
        
        db.add(place_info)
        db.commit()
    
    finally:
        db.close()
        
        
def save_place_review(review_id, user_id, nickname, contents, rating, updated_at, place_id, place_name, platform, task_id):
    db = SessionLocal()
    try:
                
        if platform == 'naver':
            place_review = NaverReview(
                review_id = review_id,
                user_id = user_id, 
                nickname = nickname,
                contents = contents,
                rating = rating,
                updated_at = updated_at,
                place_id = place_id,
                place_name = place_name,
                platform = platform,
                task_id = task_id
            )
            
        if platform == 'kakao':
            place_review = KakaoReview(
                review_id = review_id,
                user_id = user_id, 
                nickname = nickname,
                contents = contents,
                rating = rating,
                updated_at = updated_at,
                place_id = place_id,
                place_name = place_name,
                platform = platform,
                task_id = task_id
            )
            
        
        db.add(place_review)
        db.commit()
        
    except Exception as e:
        print(f"DB (review) failed: {e}")
    
    finally:
        db.close()
        