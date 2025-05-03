import os

KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'
KAFKA_TOPIC = 'place_review_ids'

DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'dbpw123!',
    'database': 'scraper'
}

NAVER_PLACE_INFO_URL = 'https://map.naver.com/p/api/search/allSearch?query='
NAVER_PLACE_REVIEW_URL = 'https://pcmap-api.place.naver.com/graphql'


#NAVER_PLACE_INFO_HEADERS = {
#    "Referer": f'https://map.naver.com/p/search/{place_quote}?c=15.00,0,0,0,dh',
#    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15'
#}

NAVER_PLACE_REVIEW_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ko',
    'Content-Type': 'application/json',
    'Origin': 'https://pcmap.place.naver.com',
    'Priority': 'u=1, i',
    #'Referer': f'https://pcmap.place.naver.com/place/{placeId}/review/visitor?additionalHeight=76&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202504271841',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    'x-ncaptcha-violation': 'true',
    'x-wtm-graphql': 'eyJhcmciOiIxNTU0NTA3NDQ2IiwidHlwZSI6InBsYWNlIiwic291cmNlIjoicGxhY2UifQ',
    # 'cookie': 'PLACE_LANGUAGE=ko; NNB=OSZ3ULFOWMGGQ; NAC=HXFpBkwrLBPR; NACT=1; SRT30=1745746879; SRT5=1745746879; BUC=o3XrRbSdN03Gy2If1q0wJUfKwA_4EpmggmqCDwiYMew=',
    }

NAVER_PLACE_REVIEW_PAYLOAD = {
        "operationName": "getVisitorReviews",
        "variables": {
            "input": {
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