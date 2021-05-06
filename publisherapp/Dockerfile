FROM debian:10

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r /requirements.txt
