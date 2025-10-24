#!/bin/sh
# Start script para compatibilidad con Dockerfile
# Lanza uvicorn respetando la variable $PORT

set -e

PORT=${PORT:-8000}
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers
#uwu
