import requests
import json
from bs4 import BeautifulSoup
import urllib


def scrape_naver_place_info(place_quote: str, start_date, end_date) -> dict:
    
    headers = {
        "referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
        #"referer": f'https://map.naver.com/p/search/{place_quote}/place/1554507446?c=15.00,0,0,0,dh&isCorrectAnswer=true',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
    }

    n_in_url = f'https://map.naver.com/p/api/search/allSearch?query={place_quote}&type=all&searchCoord=126.855804%3B37.524546&boundary='
    print(n_in_url)

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

def scrape_naver_place_review(place_quote: str) -> dict:
    place_id = scrape_naver_place_info(place_quote)['place_id']
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
        'referer': f'https://pcmap.place.naver.com/place/{place_id}/review/visitor?additionalHeight=76&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202504271841',
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
                'channelId': place_id,
                'input': {
                    'channelId': place_id,
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
                    'businessId': place_id,
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
                'id': place_id,
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
                'businessId': place_id,
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
                    'businessId': place_id,
                },
            },
            'query': 'query getFollowingReviews($input: FollowingReviewsInput) {\n  followingReviews(input: $input) {\n    reviews {\n      id\n      apolloCacheId\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        theme {\n          totalCount\n          __typename\n        }\n        isFollowing\n        followerCount\n        followRequested\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        thumbnailRatio\n        class\n        videoId\n        videoUrl\n        trailerUrl\n        __typename\n      }\n      tags\n      status\n      visitCount\n      viewCount\n      visited\n      created\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        date\n        replyTitle\n        isReported\n        isSuspended\n        status\n        __typename\n      }\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      businessName\n      votedKeywords {\n        code\n        iconCode\n        name\n        iconUrl\n        __typename\n      }\n      visitCategories {\n        code\n        name\n        keywords {\n          code\n          name\n          __typename\n        }\n        __typename\n      }\n      userIdno\n      loginIdno\n      reactionStat {\n        id\n        typeCount {\n          name\n          count\n          __typename\n        }\n        totalCount\n        __typename\n      }\n      hasViewerReacted {\n        id\n        reacted\n        __typename\n      }\n      nickname\n      representativeVisitDateTime\n      __typename\n    }\n    reactionTypes {\n      name\n      emojiUrl\n      label\n      __typename\n    }\n    __typename\n  }\n}',
        },
        {
            'operationName': 'getVisitorRatingReviews',
            'variables': {
                'input': {
                    'businessId': place_id,
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
                    'businessId': place_id,
                    'page': 1,
                    'display': 3,
                },
            },
            'query': 'query getVisitorReviewThemeLists($input: ThemeListsInput) {\n  themeLists(input: $input) {\n    themeLists {\n      id\n      title\n      viewCount\n      itemCount\n      reviews {\n        businessName\n        reviewBody\n        imageUrl\n        __typename\n      }\n      authorNickname\n      authorImageUrl\n      isFollowing\n      themeListUrl\n      authorUrl\n      __typename\n    }\n    total\n    __typename\n  }\n}',
        },
    ]

    req = requests.post('https://pcmap-api.place.naver.com/graphql', cookies=cookies, headers=headers, json=json_data)
    html = req.text
    data = json.loads(html)

    # 방문자리뷰 위치
    # data[2]

    place_reviews = []

    for cont_idx in range(len(data[2]['data']['visitorReviews']['items'])):
        place_review = {
            'user_id': data[2]['data']['visitorReviews']['items'][cont_idx]['author']['id'],
            'user_nickname': data[2]['data']['visitorReviews']['items'][cont_idx]['author']['nickname'],
            'contents': data[2]['data']['visitorReviews']['items'][cont_idx]['body'],
            'update_at': data[2]['data']['visitorReviews']['items'][cont_idx]['representativeVisitDateTime'],
            'place_id': place_id,
            'name': data[2]['data']['businessName']
        }
        
        place_reviews.append(place_review)
    
    print(place_review)

    return place_review