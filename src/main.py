import time
from datetime import datetime, timedelta
from naver_scraper import scrape_naver_place_info
# from message_queue import consume_messages, publish_message
# from database import get_db
import urllib

if __name__ == "__main__":
    # 예시: 여러 식당 이름을 리스트로 관리
    place_names = [
        "바틀드",
        "장안닭갈비 강남점",
        # "다른식당2",
        # ...
    ]

    for place_name in place_names:
        place_quote = urllib.parse.quote(place_name)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 2)
        scrape_naver_place_info(place_quote, start_date, end_date)

    # # 컨슈머 시작
    # consume_messages(message_callback)