from src.scraper.naver_scraper import scrape_naver_place_info, scrape_naver_place_review


if __name__ == '__main__':
    
    try:
        scrape_naver_place_info('바틀드')
    except Exception as e:
        print(f" naver place (info) scraping failed: {e}")
        
    try:
        scrape_naver_place_review('바틀드', '2023-01-01')
    except Exception as e:
        print(f" naver place (review) failed: {e}")