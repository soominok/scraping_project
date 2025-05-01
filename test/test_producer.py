from src.kafka.producer import enqueue_collection_task



if __name__ == "__main__":
    
    jobs = [
        {'platform': 'naver', 'place_name': '바틀드', 'start_date': '2022-01-01', 'end_date': '2024-01-01'}
    ]
    
    enqueue_collection_task('naver', '바틀드', '2022-01-01', '2024-01-01')
