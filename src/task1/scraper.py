import requests
import json
from bs4 import BeautifulSoup 
import urllib

from config import NAVER_PLACE_INFO_URL, NAVER_PLACE_REVIEW_URL, KAKAO_PLACE_INFO_URL, KAKAO_PLACE_REVIEW_URL

def scrape_naver_place_info(place_nm: str) -> dict:
    kor_quote = urllib.parse.quote(place_nm)
    
    headers = {
    "referer": f'https://map.naver.com/p/search/{query}/place/1554507446?c=15.00,0,0,0,dh&isCorrectAnswer=true',
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    }
    
    #url = f'https://map.naver.com/p/api/search/allSearch?query={kor_quote}&type=all&searchCoord=126.855804%3B37.524546&boundary='
    req = requests.get(NAVER_PLACE_INFO_URL, headers=headers)
    html = req.text

    data = json.loads(html)

    # list가 1개가 아닌 경우 예외처리 필요
    #data['result']['place']['list'][0]['id']

    print('id: ', data['result']['place']['list'][0]['id'])
    print('이름: ', data['result']['place']['list'][0]['name'])
    print('전화번호: ',  data['result']['place']['list'][0]['tel'])
    print('주소: ',  data['result']['place']['list'][0]['address'])
    print('카테고리', data['result']['place']['list'][0]['category'])
    
    
def scrape_kakao_place_info(store_name: str) -> dict:
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'pf': 'web',
    'priority': 'u=1, i',
    'referer': f'https://place.map.kakao.com/{placeId}',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    # 'cookie': 'webid=0296fdfa779647ada4e55d7e0b4debf8; webid_ts=1745665477366; __T_=1; __T_SECURE=1; JSESSIONID=42C10553B313F8C1BDB8A9419652F361; __T_=1; __T_SECURE=1; _T_ANO=m4bVO9IW6OuDb+3e9AZbY6n6JvYGB83UYKGhBjr+wbcas3s+dco7RMufJZaWyAsKdCACmGopksPYUlavtzEcEeNVi96exOFrCMFG6PjtpJzlcSIl3nnWeqzRRUCmhFyXNorkaEdgJfs4h9WihSz0CNf/jiO1YDiO9e0Cae5Uz2mS/sbqDANo1IOhpC3Gp2z/UG3aM4t+odRJlSIbBGgJPzQ3bDOyea49ffsyWcT2bJQzY3nKmWomX5A7ZUGIC/r06vvrK6p80gcbjJnlOBLuhRNxaEAPE8sfeSQQhpKnWDEXbk6UL3Nl/dLvaAXIWBzaCeD27sMHCkVnQu/pf579+g==',
    }


    #k_info_url = 'https://place-api.map.kakao.com/places/panel3/1247290145'
    req = requests.get(KAKAO_PLACE_INFO_URL, headers = headers)
    print(req)
    html = req.text

    data = json.loads(html)


    print('id: ', data['summary']['confirm_id'])
    print('이름: ', data['summary']['name'])
    print('전화번호: ',  data['summary']['phone_numbers'][0]['tel'])
    print('주소: ',  data['summary']['address']['disp'])
    print('카테고리: ', data['summary']['category']['name'])


def scrape_naver_place_review(store_name: str) -> dict:
    cookies = {
        'PLACE_LANGUAGE': 'ko',
        'NNB': 'OSZ3ULFOWMGGQ',
        'NAC': 'HXFpBkwrLBPR',
        'NACT': '1',
        'SRT30': '1745746879',
        'SRT5': '1745746879',
        'BUC': 'o3XrRbSdN03Gy2If1q0wJUfKwA_4EpmggmqCDwiYMew=',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ko',
        'content-type': 'application/json',
        'origin': 'https://pcmap.place.naver.com',
        'priority': 'u=1, i',
        'referer': f'https://pcmap.place.naver.com/place/{query}/review/visitor?additionalHeight=76&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202504271841',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'x-ncaptcha-violation': 'true',
        'x-wtm-graphql': 'eyJhcmciOiIxNTU0NTA3NDQ2IiwidHlwZSI6InBsYWNlIiwic291cmNlIjoicGxhY2UifQ',
        # 'cookie': 'PLACE_LANGUAGE=ko; NNB=OSZ3ULFOWMGGQ; NAC=HXFpBkwrLBPR; NACT=1; SRT30=1745746879; SRT5=1745746879; BUC=o3XrRbSdN03Gy2If1q0wJUfKwA_4EpmggmqCDwiYMew=',
    }

    json_data = [
        {
            'operationName': 'getPromotions',
            'variables': {
                'channelId': '1554507446',
                'input': {
                    'channelId': '1554507446',
                },
                'isBooking': False,
            },
            'query': 'query getPromotions($channelId: String, $input: PromotionInput, $isBooking: Boolean!) {\n  naverTalk @skip(if: $isBooking) {\n    alarm(channelId: $channelId) {\n      friendYn\n      validation\n      __typename\n    }\n    __typename\n  }\n  promotionCoupons(input: $input) {\n    total\n    naverId\n    coupons {\n      promotionSeq\n      placeSeq\n      couponSeq\n      userCouponSeq\n      promotionTitle\n      conditionType\n      couponUseType\n      title\n      description\n      type\n      expiredDateDescription\n      status\n      image {\n        url\n        width\n        height\n        desc\n        __typename\n      }\n      downloadableCountInfo\n      expiredPeriodInfo\n      subExpiredPeriodInfo\n      usedConditionInfos\n      couponButtonText\n      daysBeforeCouponStartDate\n      usableLandingUrl {\n        useSiteUrl\n        useBookingUrl\n        useOrderUrl\n        __typename\n      }\n      couponUsableDetail {\n        isImpPlace\n        isImpBooking\n        isImpOrder\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getMyPlaceProfile',
            'variables': {},
            'query': 'query getMyPlaceProfile {\n  user {\n    partnerHashedIdNo\n    myplace {\n      profile {\n        imageUrl\n        borderImageUrl\n        myplaceId\n        myplaceNickname\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorReviews',
            'variables': {
                'input': {
                    'businessId': '1554507446',
                    'businessType': 'place',
                    'item': '0',
                    'bookingBusinessId': '1059434',
                    'page': 1,
                    'size': 10,
                    'isPhotoUsed': False,
                    'includeContent': True,
                    'getUserStats': True,
                    'includeReceiptPhotos': True,
                    'cidList': [
                        '223563',
                        '223565',
                        '223611',
                        '223913',
                    ],
                    'getReactions': True,
                    'getTrailer': True,
                },
            },
            'query': 'query getVisitorReviews($input: VisitorReviewsInput) {\n  visitorReviews(input: $input) {\n    items {\n      id\n      reviewId\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        borderImageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        theme {\n          totalCount\n          __typename\n        }\n        isFollowing\n        followerCount\n        followRequested\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        thumbnailRatio\n        class\n        videoId\n        videoUrl\n        trailerUrl\n        __typename\n      }\n      tags\n      status\n      visitCount\n      viewCount\n      visited\n      created\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        date\n        replyTitle\n        isReported\n        isSuspended\n        status\n        __typename\n      }\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      language\n      highlightRanges {\n        start\n        end\n        __typename\n      }\n      apolloCacheId\n      translatedText\n      businessName\n      showBookingItemName\n      bookingItemName\n      votedKeywords {\n        code\n        iconUrl\n        iconCode\n        name\n        __typename\n      }\n      userIdno\n      loginIdno\n      receiptInfoUrl\n      reactionStat {\n        id\n        typeCount {\n          name\n          count\n          __typename\n        }\n        totalCount\n        __typename\n      }\n      hasViewerReacted {\n        id\n        reacted\n        __typename\n      }\n      nickname\n      showPaymentInfo\n      visitCategories {\n        code\n        name\n        keywords {\n          code\n          name\n          __typename\n        }\n        __typename\n      }\n      representativeVisitDateTime\n      showRepresentativeVisitDateTime\n      __typename\n    }\n    starDistribution {\n      score\n      count\n      __typename\n    }\n    hideProductSelectBox\n    total\n    showRecommendationSort\n    itemReviewStats {\n      score\n      count\n      itemId\n      starDistribution {\n        score\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorReviewStats',
            'variables': {
                'businessType': 'place',
                'id': '1554507446',
                'itemId': '0',
            },
            'query': 'query getVisitorReviewStats($id: String, $itemId: String, $businessType: String = "place") {\n  visitorReviewStats(\n    input: {businessId: $id, itemId: $itemId, businessType: $businessType}\n  ) {\n    id\n    name\n    apolloCacheId\n    review {\n      avgRating\n      totalCount\n      scores {\n        count\n        score\n        __typename\n      }\n      starDistribution {\n        count\n        score\n        __typename\n      }\n      imageReviewCount\n      authorCount\n      maxSingleReviewScoreCount\n      maxScoreWithMaxCount\n      __typename\n    }\n    analysis {\n      themes {\n        code\n        label\n        count\n        __typename\n      }\n      menus {\n        code\n        label\n        count\n        __typename\n      }\n      votedKeyword {\n        totalCount\n        reviewCount\n        userCount\n        details {\n          category\n          code\n          iconUrl\n          iconCode\n          displayName\n          count\n          previousRank\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    visitorReviewsTotal\n    ratingReviewsTotal\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getReactionTypes',
            'variables': {},
            'query': 'query getReactionTypes {\n  reactionTypes {\n    name\n    emojiUrl\n    label\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorReviewPhotosInVisitorReviewTab',
            'variables': {
                'businessId': '1554507446',
                'businessType': 'place',
                'item': '0',
                'page': 1,
                'size': 20,
            },
            'query': 'query getVisitorReviewPhotosInVisitorReviewTab($businessId: String!, $businessType: String, $page: Int, $size: Int, $theme: String, $item: String) {\n  visitorReviews(\n    input: {businessId: $businessId, businessType: $businessType, page: $page, size: $size, theme: $theme, item: $item, isPhotoUsed: true, includeReceiptPhotos: false, getTrailer: true}\n  ) {\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        borderImageUrl\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        thumbnailRatio\n        videoId\n        videoUrl\n        trailerUrl\n        __typename\n      }\n      tags\n      status\n      visited\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      businessName\n      isFollowing\n      visitCount\n      votedKeywords {\n        code\n        iconUrl\n        iconCode\n        name\n        __typename\n      }\n      __typename\n    }\n    starDistribution {\n      score\n      count\n      __typename\n    }\n    hideProductSelectBox\n    total\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getFollowingReviews',
            'variables': {
                'input': {
                    'businessId': '1554507446',
                },
            },
            'query': 'query getFollowingReviews($input: FollowingReviewsInput) {\n  followingReviews(input: $input) {\n    reviews {\n      id\n      apolloCacheId\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        theme {\n          totalCount\n          __typename\n        }\n        isFollowing\n        followerCount\n        followRequested\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        thumbnailRatio\n        class\n        videoId\n        videoUrl\n        trailerUrl\n        __typename\n      }\n      tags\n      status\n      visitCount\n      viewCount\n      visited\n      created\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        date\n        replyTitle\n        isReported\n        isSuspended\n        status\n        __typename\n      }\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      businessName\n      votedKeywords {\n        code\n        iconCode\n        name\n        iconUrl\n        __typename\n      }\n      visitCategories {\n        code\n        name\n        keywords {\n          code\n          name\n          __typename\n        }\n        __typename\n      }\n      userIdno\n      loginIdno\n      reactionStat {\n        id\n        typeCount {\n          name\n          count\n          __typename\n        }\n        totalCount\n        __typename\n      }\n      hasViewerReacted {\n        id\n        reacted\n        __typename\n      }\n      nickname\n      representativeVisitDateTime\n      __typename\n    }\n    reactionTypes {\n      name\n      emojiUrl\n      label\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorRatingReviews',
            'variables': {
                'input': {
                    'businessId': '1554507446',
                    'businessType': 'place',
                    'item': '0',
                    'bookingBusinessId': '1059434',
                    'page': 1,
                    'size': 10,
                    'includeContent': False,
                    'getUserStats': True,
                    'includeReceiptPhotos': True,
                    'cidList': [
                        '223563',
                        '223565',
                        '223611',
                        '223913',
                    ],
                    'getReactions': True,
                    'getTrailer': True,
                },
            },
            'query': 'query getVisitorRatingReviews($input: VisitorReviewsInput) {\n  visitorReviews(input: $input) {\n    total\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        borderImageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        theme {\n          totalCount\n          __typename\n        }\n        isFollowing\n        followerCount\n        followRequested\n        __typename\n      }\n      visitCount\n      visited\n      originType\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        date\n        replyTitle\n        isReported\n        isSuspended\n        status\n        __typename\n      }\n      votedKeywords {\n        code\n        iconUrl\n        iconCode\n        displayName\n        name\n        __typename\n      }\n      businessName\n      status\n      userIdno\n      loginIdno\n      receiptInfoUrl\n      reactionStat {\n        id\n        typeCount {\n          name\n          count\n          __typename\n        }\n        totalCount\n        __typename\n      }\n      hasViewerReacted {\n        id\n        reacted\n        __typename\n      }\n      nickname\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorReviewThemeLists',
            'variables': {
                'input': {
                    'businessId': '1554507446',
                    'page': 1,
                    'display': 3,
                },
            },
            'query': 'query getVisitorReviewThemeLists($input: ThemeListsInput) {\n  themeLists(input: $input) {\n    themeLists {\n      id\n      title\n      viewCount\n      itemCount\n      reviews {\n        businessName\n        reviewBody\n        imageUrl\n        __typename\n      }\n      authorNickname\n      authorImageUrl\n      isFollowing\n      themeListUrl\n      authorUrl\n      __typename\n    }\n    total\n    __typename\n  }\n}',
        },
    ]
    n_re_url = NAVER_PLACE_REVIEW_URL
    
    req = requests.post(n_re_url, cookies=cookies, headers=headers, json=json_data)
    html = req.text
    data = json.loads(html)

    # 방문자리뷰 위치
    # data[2]

    for cont_idx in range(len(data[2]['data']['visitorReviews']['items'])):
        print('user_id: ', data[2]['data']['visitorReviews']['items'][cont_idx]['author']['id'])
        print('user_nickname: ', data[2]['data']['visitorReviews']['items'][cont_idx]['author']['nickname'])
        print('update_at: ', data[2]['data']['visitorReviews']['items'][cont_idx]['representativeVisitDateTime'])
        # print('star_rating: ', data[2]['data']['visitorReviews'])
        print('contents:  ', data[2]['data']['visitorReviews']['items'][cont_idx]['body'])
        print('-' * 10)

def scrape_kakao_place_review(store_name: str) -> dict:
    cookies = {
        'webid': '0296fdfa779647ada4e55d7e0b4debf8',
        'webid_ts': '1745665477366',
        '__T_': '1',
        '__T_SECURE': '1',
        '_T_ANO': 'NwXmsFHED0wSqKTz/RjAPTOP7Dg8SYgyQmh7CYaV2y+ZLB/kHHDOq0wPAhoBEFfZTV1BJGo536vw1PIkvmtJ/igsla4jTM4smZk+c22KDAGDgNlijZn2vRJ4blCEJKy47oYAAzkX9S8lPioS6SitcVfmeGedpPQ1K/5BQjHpETJkn+iFAEu0d2MKjx9S5T2yxfPF0EjPxUWGvZ2bWCWH9OnKJDv81K59787KcpwCNaYd0f5pLXDihhij0ciP86AjKpcVX4kp0LVS+OQl1Mh9UiJamrlH3QRNWtZUdXfIoGpp+luhbi6V4NM+Ws5fQLzWX7D+cE/MliH+nFdLsN9FRQ==',
    }

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


    #headers = {}

    k_re_url = KAKAO_PLACE_REVIEW_URL

    req = requests.get(k_re_url, headers = headers)
    html = req.text

    data = json.loads(html)
    len(data['reviews'])#

    for idx in range(len(data['reviews'])):
        print('user_id: ', data['reviews'][idx]['meta']['owner']['map_user_id'])
        print('user_nickname: ', data['reviews'][idx]['meta']['owner']['nickname'])
        print('update_at: ', data['reviews'][idx]['updated_at'])
        print('star_rating: ', data['reviews'][idx]['star_rating'])
        print('contents:  ', data['reviews'][idx]['contents'])
        print('-' * 10)