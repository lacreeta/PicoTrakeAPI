FROM python:3.10-slim

# Exponer el puerto para HTTPS
EXPOSE 443
EXPOSE 80

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY start.sh .

CMD ["sh", "start.sh"]