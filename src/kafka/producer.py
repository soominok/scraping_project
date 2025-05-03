from confluent_kafka import Producer
import json
import uuid
from src.utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from src.db.db import init_db
from datetime import datetime, timedelta
import sys


producer_config = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
producer = Producer(producer_config)

def enqueue_place(platform, place_name, start_date):
    task_id = str(uuid.uuid4())
    
    msg = {
        'task_id': task_id,
        'platform': platform,
        'place_name': place_name,
        'start_date': start_date
        }
    

    try:
        
        producer.produce(
            topic =  'scraper-tasks',
            key = place_name,
            value = json.dumps(msg, default=str),
            callback=lambda err, msg: (
                    print(f"Delivery failed: {err}") if err else None
            )
        )
        
        producer.flush()
        
    except BufferError:
        print("Producer queue full")
    except Exception as e:
        print(f"Critical error: {str(e)}")
    
    
    print(f"Enqueued task: {msg}")
    

def enqueue_tasks(platform, place_name, init_mode = True): #
    today = datetime.today().date()
    
    if init_mode:
        start_date = (datetime.today() - timedelta(1) - timedelta(days=730)).strftime("%Y-%m-%d")
    else:
        start_date = str(today)
    
    try:    
        enqueue_place(platform, place_name, start_date)   
 
    except BufferError:
        print("Producer queue full")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        

from confluent_kafka.admin import AdminClient, NewTopic


def check_topic_exists(topic_name, num_partitions=3, replication_factor=1, bootstrap_servers="kafka:9092"):
    admin = AdminClient({'bootstrap.servers': bootstrap_servers})

    topic_metadata = admin.list_topics(timeout=5)
    if topic_name in topic_metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
        return
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    fs = admin.create_topics([new_topic])
    for topic, f in fs.items():
        try:
            f.result() 
            print(f"Topic '{topic}' created.")
        except Exception as e:
            print(f"Failed to create topic '{topic}': {e}")



if __name__ == "__main__":
    init_db()
    
    check_topic_exists("scraper-tasks")
    
    jobs = [
        {'platform': 'naver', 'place_name': '바틀드'},
        {'platform': 'kakao', 'place_name': '바틀드'},
        {'platform': 'naver', 'place_name': '장인닭갈비 강남점'},
        {'platform': 'kakao', 'place_name': '장인닭갈비 강남점'}
    ]
  
    
    for job in jobs:

        init_mode = "--init" in sys.argv
        print(init_mode)
        try:
 
            enqueue_tasks(job['platform'], job['place_name'])
            print(f"{job['platform']}+{job['place_name']} producer 완료")
        except:
            print(f"{job['platform']}+{job['place_name']} error")
            
    print('enqueue_task 실행 완료')
        