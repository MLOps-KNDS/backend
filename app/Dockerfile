FROM continuumio/anaconda3:latest

ENV API_PORT=8000
ENV API_HOST=0.0.0.0

WORKDIR /app

# Install docker
RUN curl -fsSL https://get.docker.com | sh

RUN conda create -n virtualenv python=3.11

COPY requirements.txt .

RUN conda run -n virtualenv --no-capture-output pip install -r requirements.txt

COPY logging.yaml .

COPY api .

CMD conda run -n virtualenv --no-capture-output \
        python -m uvicorn main:app \
            --host $API_HOST \
            --port $API_PORT \
            --log-config logging.yaml \
