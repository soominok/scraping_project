import requests
import json

# from config import NAVER_PLACE_INFO_URL

def fetch_place_data(query: str):
    """
    네이버 플레이스 API를 사용하여 특정 장소의 데이터를 가져옵니다.
    """
    params = {
        "query": query
        # , "type": "place"
    }
    headers = {
        "referer": f'https://map.naver.com/p/search/{query}/place/1554507446?c=15.00,0,0,0,dh&isCorrectAnswer=true',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    }
    n_info_url = f"https://map.naver.com/p/api/search/allSearch?query={query}&type=all&searchCoord=126.855804%3B37.524546&boundary="
    
    response = requests.get(n_info_url, params=params, headers=headers)
    print(response)
    
    html = response.text
    # response.raise_for_status()
    # return json.loads(html)
    
    data = json.loads(html)

    print(data)

    place_info = {
        "place_id": data['result']['place']['list'][0]['id'],
        "name": data['result']['place']['list'][0]['name'],
        "address": data['result']['place']['list'][0]['address'],
        "phone_number": data['result']['place']['list'][0]['tel']
        # , "naver_url": item.get("naverBookingUrl"),
        #"kakao_url": item.get("homePageUrl"),
    }
    
    print(place_info)
    
    return place_info

def parse_place_data(data: dict):
    """
    API 응답에서 필요한 정보를 추출합니다.
    """
    items = data.get("result", [])
    print(data)
    # print(data['result'])
    if not data:
        print("No items found in response.")
        return None
    
    # item = items[0]
    
    #place_info = {
    #    "place_id": item['place']['list'][0]['id'],
    #    "name": item['place']['list'][0]['name'],
    #    "address": item['place']['list'][0]['address'],
    #    "phone_number": item['place']['list'][0]['tel']
    #    # , "naver_url": item.get("naverBookingUrl"),
    #    #"kakao_url": item.get("homePageUrl"),
    #}
    
    place_info = {
        "place_id": data['result']['place']['list'][0]['id'],
        "name": data['result']['place']['list'][0]['name'],
        "address": data['result']['place']['list'][0]['address'],
        "phone_number": data['result']['place']['list'][0]['tel']
        # , "naver_url": item.get("naverBookingUrl"),
        #"kakao_url": item.get("homePageUrl"),
    }
    return place_info

def perform_scraping(target_place_name: str):
    """
    전체 웹 스크래핑 프로세스를 수행합니다.
    """
    try:
        data = fetch_place_data(target_place_name)
        place_info = parse_place_data(data)
        print("=== 수집된 데이터 ===")
        print(place_info)
        print("===================")
    except Exception as e:
        print(f"스크래핑 작업 실패: {e}")