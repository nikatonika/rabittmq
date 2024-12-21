FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
COPY model.py . 
COPY model.pkl .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "model.py"]
