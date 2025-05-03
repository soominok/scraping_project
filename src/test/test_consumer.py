from src.kafka.consumer import process_message



if __name__ == '__main__':
    try:
        process_message(
            msg = {
                'task_id': 't12345',
                'platform': 'naver',
                'place_name': '채선당',
                'start_date': '2021-01-11'
            }
        )
    except Exception as e:
        print(f'consumer fail: {e}')