from confluent_kafka import Producer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from kafka.producer import scrape_naver_place_info

def produce_message(producer, topic, message):
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()


def main():
    kafka_broker = KAFKA_BOOTSTRAP_SERVERS # 'kafkaIP:9092'
    topic = KAFKA_TOPIC

    # Kafka producer 설정
    producer_config = {
        'bootstrap.servers': kafka_broker
    }

    # Kafka producer 생성
    producer = Producer(producer_config)

    # 보낼 메시지

    jobs = [
        {"platform": "naver", "place_id": scrape_naver_place_info['place_id']}
    ]


    for job in jobs:


        message = "Naver Place Scraping"
        print(f"topic : {topic}, msg: {message}")
        produce_message(producer, topic, message)

if __name__ == "__main__":
    main()