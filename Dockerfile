# Dockerfile - Module 1 (Conversion)
FROM python:3.11-slim

# Install system deps and LibreOffice
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libreoffice-writer libreoffice-impress libreoffice-calc libreoffice-common \
       libreoffice-core poppler-utils fonts-dejavu-core ca-certificates wget \
       ghostscript \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Create runtime directories
RUN mkdir -p /app/uploads /app/converted

ENV PORT=8000
EXPOSE 8000

# Production server
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
