FROM python:3.10-slim

# Exponer el puerto para HTTPS
EXPOSE 443
EXPOSE 80

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


COPY . .

COPY ./ssl/cert.pem /app/ssl/cert.pem
COPY ./ssl/key.pem /app/ssl/key.pem

RUN chmod +x start.sh

CMD ["sh", "start.sh"]