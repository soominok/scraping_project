import requests
import urllib
import json
from dotenv import load_dotenv
import os

load_dotenv()



def scrape_kakao_place_info(place_name:str) -> dict:
    # place_id = place_quote # 임시
    

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
    
    place_id = api_data['documents'][0]['id']
    print(place_id)
    
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
        # 'cookie': 'webid=0296fdfa779647ada4e55d7e0b4debf8; webid_ts=1745665477366; __T_=1; __T_SECURE=1; JSESSIONID=42C10553B313F8C1BDB8A9419652F361; __T_=1; __T_SECURE=1; _T_ANO=m4bVO9IW6OuDb+3e9AZbY6n6JvYGB83UYKGhBjr+wbcas3s+dco7RMufJZaWyAsKdCACmGopksPYUlavtzEcEeNVi96exOFrCMFG6PjtpJzlcSIl3nnWeqzRRUCmhFyXNorkaEdgJfs4h9WihSz0CNf/jiO1YDiO9e0Cae5Uz2mS/sbqDANo1IOhpC3Gp2z/UG3aM4t+odRJlSIbBGgJPzQ3bDOyea49ffsyWcT2bJQzY3nKmWomX5A7ZUGIC/r06vvrK6p80gcbjJnlOBLuhRNxaEAPE8sfeSQQhpKnWDEXbk6UL3Nl/dLvaAXIWBzaCeD27sMHCkVnQu/pf579+g==',
    }
    
    
    k_in_url = f'https://place-api.map.kakao.com/places/panel3/{place_id}'
    req = requests.get(k_in_url, headers = headers)
    html = req.text

    data = json.loads(html)
    # print(data)
    
    kakao_info = {
        "place_id": data["summary"]["confirm_id"],
        "place_name": data["summary"]["name"],
        "address": data["summary"]["address"]["disp"],
        "tel": data["summary"]["phone_numbers"][0]["tel"],
        "platform": 'kakao'
    }
    
    print(kakao_info)


    return kakao_info


def scrape_kakao_place_review(place_name:str, start_date) -> dict:
    
    place_id = scrape_kakao_place_info(place_name)['place_id']
    
    # cookies = {
    #     'webid': '0296fdfa779647ada4e55d7e0b4debf8',
    #     'webid_ts': '1745665477366',
    #     '__T_': '1',
    #     '__T_SECURE': '1',
    #     '_T_ANO': 'NwXmsFHED0wSqKTz/RjAPTOP7Dg8SYgyQmh7CYaV2y+ZLB/kHHDOq0wPAhoBEFfZTV1BJGo536vw1PIkvmtJ/igsla4jTM4smZk+c22KDAGDgNlijZn2vRJ4blCEJKy47oYAAzkX9S8lPioS6SitcVfmeGedpPQ1K/5BQjHpETJkn+iFAEu0d2MKjx9S5T2yxfPF0EjPxUWGvZ2bWCWH9OnKJDv81K59787KcpwCNaYd0f5pLXDihhij0ciP86AjKpcVX4kp0LVS+OQl1Mh9UiJamrlH3QRNWtZUdXfIoGpp+luhbi6V4NM+Ws5fQLzWX7D+cE/MliH+nFdLsN9FRQ==',
    # }

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
        # 'cookie': 'webid=0296fdfa779647ada4e55d7e0b4debf8; webid_ts=1745665477366; __T_=1; __T_SECURE=1; _T_ANO=NwXmsFHED0wSqKTz/RjAPTOP7Dg8SYgyQmh7CYaV2y+ZLB/kHHDOq0wPAhoBEFfZTV1BJGo536vw1PIkvmtJ/igsla4jTM4smZk+c22KDAGDgNlijZn2vRJ4blCEJKy47oYAAzkX9S8lPioS6SitcVfmeGedpPQ1K/5BQjHpETJkn+iFAEu0d2MKjx9S5T2yxfPF0EjPxUWGvZ2bWCWH9OnKJDv81K59787KcpwCNaYd0f5pLXDihhij0ciP86AjKpcVX4kp0LVS+OQl1Mh9UiJamrlH3QRNWtZUdXfIoGpp+luhbi6V4NM+Ws5fQLzWX7D+cE/MliH+nFdLsN9FRQ==',
    }

    k_re_url = f'https://place-api.map.kakao.com/places/tab/reviews/kakaomap/{place_id}?order=RECOMMENDED&only_photo_review=false'

    req = requests.get(k_re_url, headers = headers)
    html = req.text

    data = json.loads(html)
    # print(data)
        
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
                'update_at': review['updated_at'],
                'place_id': place_id,
                'place_name': place_name,
                'platform': 'kakao'
            }    

            kakao_reviews.append(kakao_review)
        else:
            continue

    print('리뷰 수: ', len(kakao_reviews))

    return kakao_reviews