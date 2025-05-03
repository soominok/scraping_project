import requests
import urllib
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()



def scrape_kakao_place_info(place_name:str) -> dict:

    REST_API_KEY = os.getenv('REST_API_KEY')

    headers = {
        'Authorization' : f'KakaoAK {REST_API_KEY}'
    }    
    
    params = {
    'query': place_name
    }

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

    req = requests.get(url, headers = headers, params = params)
    html = req.text
    api_data = json.loads(html)
    print(api_data)
    time.sleep(0.1)
    place_id = api_data['documents'][0]['id']
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'pf': 'web',
        'priority': 'u=1, i',
        'referer': f'https://place.map.kakao.com/{place_id}',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    }
    
    
    k_in_url = f'https://place-api.map.kakao.com/places/panel3/{place_id}'
    req = requests.get(k_in_url, headers = headers)
    html = req.text

    data = json.loads(html)
    try:
        if len(data['summary']['phone_numbers']) > 0:
            kakao_info = {
                "place_id": data["summary"]["confirm_id"],
                "place_name": data["summary"]["name"],
                "address": data["summary"]["address"]["disp"],
                "tel": data["summary"]["phone_numbers"][0]["tel"],
                "platform": 'kakao'
            }
        else:
            kakao_info = {
                "place_id": data["summary"]["confirm_id"],
                "place_name": data["summary"]["name"],
                "address": data["summary"]["address"]["disp"],
                "tel": data["summary"]["phone_numbers"],
                "platform": 'kakao'
            }
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
    
    print(kakao_info)


    return kakao_info


def scrape_kakao_place_review(place_name:str, start_date) -> dict:
    
    place_id = scrape_kakao_place_info(place_name)['place_id']
    

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://place.map.kakao.com',
        'pf': 'web',
        'priority': 'u=1, i',
        'referer': 'https://place.map.kakao.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    }

    k_re_url = f'https://place-api.map.kakao.com/places/tab/reviews/kakaomap/{place_id}?order=RECOMMENDED&only_photo_review=false'

    req = requests.get(k_re_url, headers = headers)
    html = req.text

    data = json.loads(html)

        
    len(data['reviews'])

    kakao_reviews = []

    for  review in data['reviews']:
        
        if review['updated_at'] >= start_date:
            
            kakao_review = {
                'review_id': review['review_id'],
                'user_id': review['meta']['owner']['map_user_id'],
                'nickname': review['meta']['owner']['nickname'],
                'contents': review['contents'],
                'rating': review['star_rating'],
                'updated_at': review['updated_at'],
                'place_id': place_id,
                'place_name': place_name,
                'platform': 'kakao'
            }    

            kakao_reviews.append(kakao_review)
        else:
            continue

    print(kakao_reviews)


    return kakao_reviews

scrape_kakao_place_info('장인닭갈비 강남점')