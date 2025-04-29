# 네이버맵_info (완)

import requests
import json
import urllib
import time
from config import NAVER_PLACE_INFO_URL, NAVER_PLACE_REVIEW_URL, NAVER_PLACE_INFO_HEADERS, NAVER_PLACE_REVIEW_HEADERS


def scrape_naver_place_info(place_name, start_date, end_date):
    
    place_quote = urllib.parse.quote(place_name)
    
    #headers = {
    #    "referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
    #    #"referer": f'https://map.naver.com/p/search/{place_quote}/place/1554507446?c=15.00,0,0,0,dh&isCorrectAnswer=true',
    #    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    #}

    headers = NAVER_PLACE_INFO_HEADERS
    
    n_in_url = NAVER_PLACE_INFO_URL + f'{place_quote}&type=all&searchCoord=126.855804%3B37.524546&boundary='
    print(n_in_url)

    req = requests.get(n_in_url, headers=headers)
    html = req.text

    data = json.loads(html)

    
    naver_info = {
        'place_id': data['result']['place']['list'][0]['id'],
        "name": data['result']['place']['list'][0]['name'],
        "address": data['result']['place']['list'][0]['address'],
        "phone_number": data['result']['place']['list'][0]['tel']
        # , "naver_url": item.get("naverBookingUrl"),
        #"kakao_url": item.get("homePageUrl"),
    }
    
    print(naver_info)


    return naver_info



def scrape_naver_place_review(place_quote, start_date, end_date):
    placeId = scrape_naver_place_info(place_quote, start_date, end_date)['place_id']
    
    #url = "https://pcmap-api.place.naver.com/graphql"
    url = NAVER_PLACE_REVIEW_URL

    #headers = {
    #    'accept': '*/*',
    #        'accept-language': 'ko',
    #        'content-type': 'application/json',
    #        'origin': 'https://pcmap.place.naver.com',
    #        'priority': 'u=1, i',
    #        'referer': f'https://pcmap.place.naver.com/place/{placeId}/review/visitor?additionalHeight=76&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202504271841',
    #        'sec-fetch-dest': 'empty',
    #        'sec-fetch-mode': 'cors',
    #        'sec-fetch-site': 'same-site',
    #        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    #        'x-ncaptcha-violation': 'true',
    #        'x-wtm-graphql': 'eyJhcmciOiIxNTU0NTA3NDQ2IiwidHlwZSI6InBsYWNlIiwic291cmNlIjoicGxhY2UifQ',
    #        # 'cookie': 'PLACE_LANGUAGE=ko; NNB=OSZ3ULFOWMGGQ; NAC=HXFpBkwrLBPR; NACT=1; SRT30=1745746879; SRT5=1745746879; BUC=o3XrRbSdN03Gy2If1q0wJUfKwA_4EpmggmqCDwiYMew=',
    #}

    headers = NAVER_PLACE_REVIEW_HEADERS

    payload = {
        "operationName": "getVisitorReviews",
        "variables": {
            "input": {
                # "placeId": placeId,
                # "display": 10,
                # "start": 1,
                # "sort": "recent"
                "businessId": "1554507446",
                "businessType": "place",
                "cidList": ["223563", "223565", "223611", "223913"],
                "getReactions": True,
                "getTrailer": True,
                "getUserStats": True,
                "includeContent": True,
                "includeReceiptPhotos": True,
                "isPhotoUsed": False,
                "item": "0",
                "page": 1,
                "size": 10
            }
        },
        "query": """query getVisitorReviews($input: VisitorReviewsInput) {
            visitorReviews(input: $input) {
            items {
                id
                reviewId
                rating
                author {
                id
                nickname
                from
                imageUrl
                borderImageUrl
                objectId
                url
                review {
                    totalCount
                    imageCount
                    avgRating
                    __typename
                }
                theme {
                    totalCount
                    __typename
                }
                isFollowing
                followerCount
                followRequested
                __typename
                }
                body
                thumbnail
                media {
                type
                thumbnail
                thumbnailRatio
                class
                videoId
                videoUrl
                trailerUrl
                __typename
                }
                tags
                status
                visitCount
                viewCount
                visited
                created
                reply {
                editUrl
                body
                editedBy
                created
                date
                replyTitle
                isReported
                isSuspended
                status
                __typename
            }
            originType
            item {
                name
                code
                options
                __typename
            }
            language
            highlightRanges {
                start
                end
                __typename
            }
            apolloCacheId
            translatedText
            businessName
            showBookingItemName
            bookingItemName
            votedKeywords {
                code
                iconUrl
                iconCode
                name
                __typename
            }
            userIdno
            loginIdno
            receiptInfoUrl
            reactionStat {
                id
                typeCount {
                name
                count
                __typename
                }
                totalCount
                __typename
            }
            hasViewerReacted {
                id
                reacted
                __typename
            }
            nickname
            showPaymentInfo
            visitCategories {
                code
                name
                keywords {
                code
                name
                __typename
                }
                __typename
            }
            representativeVisitDateTime
            showRepresentativeVisitDateTime
            __typename
            }
            starDistribution {
                score
                count
                __typename
            }
            hideProductSelectBox
            total
            showRecommendationSort
            itemReviewStats {
                score
                count
                itemId
            starDistribution {
                score
                count
                __typename
            }
            __typename
            }
            __typename
        }
        }"""
    }

    naver_reviews = []
    i = 0
    
    for page in range(1, 101):  # 10개씩 100개까지
        time.sleep(0.5)
        
        payload["variables"]["input"]["page"] = page
        print('page: ', payload["variables"]["input"]["page"])
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        if res.status_code != 200:
            break
        else:
            data = res.json()
            if len(data["data"]["visitorReviews"]["items"]) == 0:
                break
            else:
                for review in data["data"]["visitorReviews"]["items"]:
                    naver_review = {
                        'review_id': 'n' + review['reviewId'],
                        'user_id': review['author']['id'],
                        'nickname': review['author']['nickname'],
                        'contents': review['body'],
                        'rating': review['rating'],
                        'update_at': review['representativeVisitDateTime'],
                        'naver_place_id': placeId,
                        'naver_place_name': review['businessName']
                    }
                    
                    naver_reviews.append(naver_review)
                
                
                    #print([i] )
                    #print(f"평점: {review['rating']}")
                    #print(f"작성자: {review['author']['nickname']}")
                    #print(f"내용: {review['body']}")
                    #print("---")
                    #i += 1
                    
    print('리뷰 수: ', len(naver_reviews))
    # print(naver_reviews)
    
    return naver_reviews
    
scrape_naver_place_review('바틀드', 20250401, 20250430)