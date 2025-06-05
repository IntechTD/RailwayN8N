
FROM python:3.11-slim

RUN apt-get update &&     apt-get install -y wget unzip gnupg2 chromium chromium-driver &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"

WORKDIR /app
COPY . /app

RUN mkdir -p /app/downloads
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "export_pme.py"]
