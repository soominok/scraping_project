KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'
KAFKA_TOPIC = 'place_review_ids'

MYSQL_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'Wjdalsdhr!33',
    'database': 'scraper'
}

NAVER_PLACE_INFO_URL = 'https://map.naver.com/p/api/search/allSearch?query='
NAVER_PLACE_REVIEW_URL = 'https://pcmap-api.place.naver.com/graphql'


NAVER_PLACE_INFO_HEADERS = {
    "Referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
}

NAVER_PLACE_REVIEW_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ko',
    'Content-Type': 'application/json',
    'Origin': 'https://pcmap.place.naver.com',
    'Priority': 'u=1, i',
    'Referer': f'https://pcmap.place.naver.com/place/{placeId}/review/visitor?additionalHeight=76&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202504271841',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    'x-ncaptcha-violation': 'true',
    'x-wtm-graphql': 'eyJhcmciOiIxNTU0NTA3NDQ2IiwidHlwZSI6InBsYWNlIiwic291cmNlIjoicGxhY2UifQ',
    # 'cookie': 'PLACE_LANGUAGE=ko; NNB=OSZ3ULFOWMGGQ; NAC=HXFpBkwrLBPR; NACT=1; SRT30=1745746879; SRT5=1745746879; BUC=o3XrRbSdN03Gy2If1q0wJUfKwA_4EpmggmqCDwiYMew=',
    }