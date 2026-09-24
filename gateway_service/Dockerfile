FROM python:3.12-slim

WORKDIR /app

COPY gateway_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY gateway_service/ .

EXPOSE 5000

CMD ["python", "app.py"]
