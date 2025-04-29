from kafka import KafkaProducer, KafkaConsumer
import json
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_NAME

def get_producer():
    return KafkaProducer(
        bootstrap_servers=['kafka:9092'],  # Docker 서비스 이름 사용
        api_version=(2, 8, 0)  # 명시적 API 버전 지정 [1][4]
    )
    
        #bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
        #value_serializer=lambda x: json.dumps(x).encode('utf-8')
    #)

def get_consumer(group_id="place_consumer_group"):
    return KafkaConsumer(
        KAFKA_TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def enqueue_message(producer, message):
    producer.send(KAFKA_TOPIC_NAME, message)