FROM python:3.10

ENV API_PORT=8000
ENV API_HOST=0.0.0.0

# Install docker
RUN curl -fsSL https://get.docker.com | sh

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY api .

CMD uvicorn main:app --host $API_HOST --port $API_PORT
