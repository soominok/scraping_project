import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://example:example@db:3306/naver_place?charset=utf8mb4"
)
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "scraping_requests")
NAVER_PLACE_INFO_URL = "https://map.naver.com/p/api/search/allSearch?query={query}&type=all&searchCoord=126.855804%3B37.524546&boundary="
NAVER_PLACE_REVIEW_URL = "https://pcmap-api.place.naver.com/graphql"
KAKAO_PLACE_INFO_URL = "https://place-api.map.kakao.com/places/panel3/{placeId}"
KAKAO_PLACE_REVIEW_URL = "https://place-api.map.kakao.com/places/tab/reviews/kakaomap/{placeId}?order=RECOMMENDED&only_photo_review=false"