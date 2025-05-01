FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


#RUN pip install --upgrade pip
#RUN pip install requests kafka-python pymongo mysql-connector-python beautifulsoup4

# CMD ["python", "main.py"]