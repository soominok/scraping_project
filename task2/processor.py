from sqlalchemy.exc import SQLAlchemyError
from db_models import ScrapingJob, PlaceData, ReviewData
from naver_scraper import scrape_naver_place_info, scrape_naver_place_review
# from .kakao_place import fetch_kakao_place_data, fetch_kakao_place_reviews
import logging
from datetime import datetime
import urllib

logger = logging.getLogger(__name__)

def process_message(session, message):
    place_nm = message.get('place_nm')
    source = message.get('source')
    target_date = message.get('target_date')

    if not place_nm or not source:
        logger.error("Invalid message format")
        return

    try:
        # Save scraping job
        job = ScrapingJob(
            place_nm=place_nm,
            source=source,
            status='InProgress'
        )
        session.add(job)
        session.commit()
        
        place_quote = urllib.quote(place_nm)
        
        # Process data
        if source == 'naver':
            place_data = scrape_naver_place_info(place_quote)
            reviews = scrape_naver_place_review(place_quote, target_date)
        # elif source == 'kakao':
        #     place_data = fetch_kakao_place_data(place_id)
        #     reviews = fetch_kakao_place_reviews(place_id, target_date)
        else:
            raise ValueError(f"Invalid source: {source}")

        # Save place data
        if place_data:
            place = session.query(PlaceData).get((place_nm, source))
            if place:
                for key, value in place_data.items():
                    setattr(place, key, value)
            else:
                place = PlaceData(
                    place_nm=place_nm,
                    source=source,
                    **place_data
                )
                session.add(place)

        # Save reviews
        if reviews:
            for review in reviews:
                existing = session.query(ReviewData).filter_by(
                    place_nm=place_nm,
                    source=source,
                    review_id=review['review_id']
                ).first()
                
                if not existing:
                    new_review = ReviewData(
                        place_nm=place_nm,
                        source=source,
                        **review
                    )
                    session.add(new_review)

        # Update job status
        job.status = 'OK'
        session.commit()

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        session.rollback()
        if job:
            job.status = 'FAILED'
            session.commit()
        raise
