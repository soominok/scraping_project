from kafka import KafkaProducer, KafkaConsumer
import json
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

def publish_message(message):
    """
    메시지를 Kafka 토픽에 발행합니다.
    message에는 target_place_name, query, place_id 등 필요한 파라미터가 포함되어야 합니다.
    """
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(KAFKA_TOPIC, message)
    producer.flush()
    producer.close()
    print(f"[Kafka] Sent: {message}")

def consume_messages(callback, group_id="scraper-group"):
    """
    Kafka 토픽에서 메시지를 소비하고 callback 함수를 호출합니다.
    callback 함수는 메시지에서 URL 파라미터를 추출하여 사용합니다.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    print("[Kafka] Waiting for messages...")
    for message in consumer:
        callback(message.value)

def get_naver_url(message):
    """
    메시지에서 query 파라미터를 추출하여 네이버 URL을 생성합니다.
    """
    from config import NAVER_PLACE_BASE_URL_TEMPLATE
    query = message.get('query', '')
    return NAVER_PLACE_BASE_URL_TEMPLATE.format(query=query)

def get_kakao_url(message):
    """
    메시지에서 place_id 파라미터를 추출하여 카카오 URL을 생성합니다.
    """
    from config import KAKAO_PLACE_BASE_URL_TEMPLATE
    place_id = message.get('place_id', '')
    return KAKAO_PLACE_BASE_URL_TEMPLATE.format(place_id=place_id)