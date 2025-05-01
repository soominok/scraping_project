from confluent_kafka import Consumer #, KafkaException
from src.db.db import log_job_status, update_job_status, save_place_info, save_place_review
from src.scraper.naver_scraper import scrape_naver_place_info, scrape_naver_place_review
from src.scraper.kakao_scraper import scrape_kakao_place_info, scrape_kakao_place_review

from src.utils.config import KAFKA_BOOTSTRAP_SERVERS
import json

import time


consumer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'place-scraper-group',
    # 'group.id': 'test-group-123',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['scraper-tasks'])

def process_message(msg):
    data = json.loads(msg.value().decode('utf-8'))
    print(data)
    
    try:    
        print(f"Received message: {data}")
        task_id = data['task_id']
        platform = data['platform']
        place_name = data['place_name']
        start_date = data['start_date']
        print('start_Date', start_date)
        
        log_job_status(task_id, 'IN_PROGRESS', platform, place_name)
        
        if platform == 'naver':
            result_info = scrape_naver_place_info(place_name)
            result_reviews = scrape_naver_place_review(place_name, start_date)
        elif platform == 'kakao':
            result_info = scrape_kakao_place_info(place_name)
            result_reviews = scrape_kakao_place_review(place_name, start_date)
        else:
            raise Exception("Unknown platform")
        
        try:
            save_place_info(result_info['place_id'], result_info['place_name'], result_info['address'], result_info['tel'], platform, task_id)
        except Exception as e:
            print(f"Info Task {task_id} failed: {e}")
            
        try:
            save_place_review(result_reviews, task_id)
        except Exception as e:
            print(f"Review Task {task_id} failed: {e}")
          
        update_job_status(task_id, 'OK')
        print(f"Task {task_id} completed.")
        
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {data}, Error: {e}")
        return
    
    except Exception as e:
        update_job_status(task_id, 'FAILED', str(e))
        print(f"Task {task_id} failed: {e}")
        
        
if __name__ == "__main__":
    
    print("Consumer started")
    
    while True:
        msg = consumer.poll(0.5)
        
        if msg is None:
            print("Waiting for message")
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        try:
            print("Saving to DB")
            process_message(msg)
            consumer.commit(msg)
            time.sleep(0.1)
        
        except Exception as e:
            print(f"Processing error: {e}")
        