from src.db.db import init_db,  log_job_status, update_job_status, save_place_info, save_place_review


if __name__ == "__main__":
    
    try:
        init_db()
    except:
        print('init db fail')
        
    try:
        log_job_status('1111', 'OK', 'naver', '바틀드', '')      
    except:
        print('log status job fail')
        
    try:
        update_job_status('2222', 'FAILED', 'No data')
    except:
        print('update status job fail')    
        
        
    try:
        save_place_info('123456', '장인닭갈비 강남점', '서울시 강남구 강남대로', '02-1234-5678', 'kakao', '1112')
    except Exception as e:
        print(f"save info Error: {e}")
    
    
    try:
        save_place_review('a12345', 'aa111', '수민', '닭갈비 너무 맛있어요!!', '3', '2025-01-02 11:00:03', '123456', 
                          '장인닭갈비 강남점', 'kakao', '서울시 강남구 강남대로', '02-1234-5678', 'kakao', '1113')
    except Exception as e:
        print(f"save review Error: {e}")
    
    