import time
from datetime import datetime, timedelta
from scraper import scrape_naver_place_info
from message_queue import consume_messages, publish_message
from database import get_db

def message_callback(message):
    db = next(get_db())
    try:
        print(f"[Kafka] Received: {message}")
        job_id = scrape_naver_place_info(db, message['target_place_name'])
        print(f"[Kafka] Scraping finished: job_id={job_id}")
    except Exception as e:
        print(f"[Kafka] Error: {e}")

def enqueue_scraping_requests(place_names, start_date: datetime, end_date: datetime):
    for place_name in place_names:
        current_date = start_date
        while current_date <= end_date:
            message = {
                "target_place_name": place_name,
                "date": current_date.strftime("%Y-%m-%d")
            }
            publish_message(message)
            current_date += timedelta(days=1)

if __name__ == "__main__":
    # 예시: 여러 식당 이름을 리스트로 관리
    place_names = [
        "만배아리랑 본점",
        # "다른식당1",
        # "다른식당2",
        # ...
    ]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)
    enqueue_scraping_requests(place_names, start_date, end_date)

    # 컨슈머 시작
    consume_messages(message_callback)