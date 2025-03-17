FROM python:3.10-slim

# Exponer el puerto para HTTPS
EXPOSE 443

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]