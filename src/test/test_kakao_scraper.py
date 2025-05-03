from src.scraper.kakao_scraper import scrape_kakao_place_info, scrape_kakao_place_review


if __name__ == '__main__':
    
    try:
        scrape_kakao_place_info('바틀드')
    except Exception as e:
        print(f" kakao place (info) scraping failed: {e}")
        
    try:
        scrape_kakao_place_review('바틀드', '2023-01-01')
    except Exception as e:
        print(f" kakao place (review) failed: {e}")