FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install requests kafka-python pymongo mysql-connector-python beautifulsoup4

CMD ["python", "main.py"]