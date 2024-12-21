FROM python:3.11-slim

ENV MPLBACKEND=Agg

WORKDIR /app

COPY . .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs


CMD ["python3", "plot.py"]
