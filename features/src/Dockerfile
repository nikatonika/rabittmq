FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY  features.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "features.py"]
