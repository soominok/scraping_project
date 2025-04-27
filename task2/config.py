import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "mysql+mysqlconnector://root:Wjdalsdhr!33@localhost/scraper"
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", 
    "localhost:9092"
)

KAFKA_TOPIC_NAME = os.getenv(
    "KAFKA_TOPIC_NAME", 
    "place_requests"
)
# NAVER_PLACE_INFO_URL = f"https://map.naver.com/p/api/search/allSearch?query={query}&type=all&searchCoord=126.855804%3B37.524546&boundary="
