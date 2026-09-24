FROM python:3.12-slim

WORKDIR /app

COPY todo_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY todo_service/ .

RUN mkdir -p /app/instance

EXPOSE 5001

CMD ["python", "app.py"]
