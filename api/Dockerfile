FROM python:3.10

ENV API_PORT=8000
ENV API_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt .
COPY src .

RUN pip install -r requirements.txt

CMD uvicorn main:app --host $API_HOST --port $API_PORT
