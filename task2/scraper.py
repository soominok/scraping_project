# 네이버맵_info (완)

import requests
import json
from bs4 import BeautifulSoup
import urllib


def scrape_naver_place_info(place_quote: str) -> dict:
    
    headers = {
        "referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
        #"referer": f'https://map.naver.com/p/search/{place_quote}/place/1554507446?c=15.00,0,0,0,dh&isCorrectAnswer=true',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    }

    n_in_url = f'https://map.naver.com/p/api/search/allSearch?query={place_quote}&type=all&searchCoord=126.855804%3B37.524546&boundary='
    
    req = requests.get(n_in_url, headers=headers)
    html = req.text

    data = json.loads(html)

    
    place_info = {
        'place_id': data['result']['place']['list'][0]['id'],
        "name": data['result']['place']['list'][0]['name'],
        "address": data['result']['place']['list'][0]['address'],
        "phone_number": data['result']['place']['list'][0]['tel']
        # , "naver_url": item.get("naverBookingUrl"),
        #"kakao_url": item.get("homePageUrl"),
    }
    
    print(place_info)

    return place_info

    print()
    print('이름: ', data['result']['place']['list'][0]['name'])
    print('전화번호: ',  data['result']['place']['list'][0]['tel'])
    print('주소: ',  data['result']['place']['list'][0]['address'])
    print('카테고리', data['result']['place']['list'][0]['category'])
