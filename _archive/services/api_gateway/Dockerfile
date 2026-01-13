FROM python:3.11-slim
WORKDIR /app

COPY services /app/services
COPY services/api_gateway /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","10000"]


