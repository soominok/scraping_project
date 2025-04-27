from message_queue import get_consumer
from db import get_db_session
from processor import process_message
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def enqueue_past_requests(producer, place_nm, source, days=730):
    """과거 2년치 데이터 수집 요청"""
    today = datetime.now()
    for i in range(days):
        target_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        message = {
            'place_nm': place_nm,
            'source': source,
            'target_date': target_date
        }
        producer.send(message)
        logger.info(f"Enqueued: {message}")

def main():
    # Initialize database
    from db import init_db
    init_db()

    # Setup consumer
    consumer = get_consumer()
    
    # Process messages
    for message in consumer:
        logger.info(f"Processing message: {message.value}")
        with get_db_session() as session:  # SQLAlchemy 세션 관리
            try:
                process_message(session, message.value)
            except Exception as e:
                logger.error(f"Failed to process message: {str(e)}")

if __name__ == "__main__":
    main()
