FROM debian:10

RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

COPY main.py main.py

CMD ["python3", "main.py"]
