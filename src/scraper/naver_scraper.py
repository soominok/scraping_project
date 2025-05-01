# 네이버맵_info (완)

import requests
import json
import urllib
import time
from src.utils.config import NAVER_PLACE_INFO_URL, NAVER_PLACE_REVIEW_URL, NAVER_PLACE_REVIEW_HEADERS, NAVER_PLACE_REVIEW_PAYLOAD #NAVER_PLACE_INFO_HEADERS, 
import re


def scrape_naver_place_info(place_name):
    
    place_quote = urllib.parse.quote(place_name)
    
    headers = {
        "referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    }

    #headers = NAVER_PLACE_INFO_HEADERS
    
    n_in_url = NAVER_PLACE_INFO_URL + f'{place_quote}&type=all&searchCoord=126.855804%3B37.524546&boundary='

    req = requests.get(n_in_url, headers=headers)
    html = req.text

    data = json.loads(html)

    
    naver_info = {
        "place_id": data["result"]["place"]["list"][0]["id"],
        "place_name": data["result"]["place"]["list"][0]["name"],
        "address": data["result"]["place"]["list"][0]["address"],
        "tel": data["result"]["place"]["list"][0]["tel"],
        # "updated_at": data["result"],
        "platform": "naver"
    }
    
    print(naver_info)

    return naver_info



def scrape_naver_place_review(place_name, start_date):
    
    place_id = scrape_naver_place_info(place_name)['place_id']
    
    url = NAVER_PLACE_REVIEW_URL
    
    
    headers = NAVER_PLACE_REVIEW_HEADERS


    NAVER_PLACE_REVIEW_PAYLOAD['variables']['input']['businessId'] = str(place_id)
    payload = NAVER_PLACE_REVIEW_PAYLOAD

    naver_reviews = []
 
    for page in range(1, 101):
        time.sleep(0.5)
        
        payload["variables"]["input"]["page"] = page
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        if res.status_code != 200:
            break
        else:
            data = res.json()
            if len(data["data"]["visitorReviews"]["items"]) == 0:
                break
            else:
                for review in data["data"]["visitorReviews"]["items"]:
                    if review["representativeVisitDateTime"] >= start_date:
                        naver_review = {
                            "review_id": review["reviewId"],
                            "user_id": review["author"]["id"],
                            "nickname": review["author"]["nickname"],
                            "contents": review["body"],
                            "rating": review["rating"],
                            "updated_at": re.sub(r'\.\d+Z$', '', review["representativeVisitDateTime"].replace('T', ' ')),
                            "place_id": place_id,
                            "place_name": review["businessName"],
                            "updated_at": review["representativeVisitDateTime"],
                            "platform": "naver" 
                        } 
                        naver_reviews.append(naver_review)
                    else:
                        continue
                    
    print('리뷰 수: ', len(naver_reviews))

    return naver_reviews
