# !/bin/sh

# HTTPS
# uvicorn main:app --host 0.0.0.0 --port 443 \
#     --ssl-keyfile /app/ssl/key.pem \
#     --ssl-certfile /app/ssl/cert.pem &

# HTTP
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
