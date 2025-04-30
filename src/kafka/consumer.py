import confluent_kafka import Consumer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from naver_scraper import scrape_naver_place_info

PLATFORM_HANDLERS = {
    "naver": scrape_naver_place_info,
    # "kakao": 
}

def consume():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'review-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([KAFKA_TOPIC])