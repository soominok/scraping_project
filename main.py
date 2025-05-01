#from kafka.producer import main
from kafka.consumer11 import consume
import urllib


place_name = '바틀드'
place_quote = urllib.parse.quote(place_name)
    

# main(place_quote, 20240101, 20240430)
consume()