from src.kafka.producer import enqueue_tasks, enqueue_place



if __name__ == "__main__":
    
    try:
        enqueue_tasks('naver', '장인닭갈비 강남점', '2022-01-01')
    except Exception as e:
        print(f" producer tasks failed: {e}")
        
    try:
        enqueue_place('naver', '장인닭갈비 강남점', '2022-01-01')
    except Exception as e:
        print(f" producer enqueue failed: {e}")
    
