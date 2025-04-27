import requests
import json
import mysql.connector
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv