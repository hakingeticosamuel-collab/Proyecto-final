# Build stage for Vue frontend
FROM node:20-bullseye AS builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Runtime stage for Flask backend
FROM python:3.13-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    build-essential \
    && mkdir -p /usr/share/keyrings \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
COPY --from=builder /app/frontend/dist ./frontend/dist

EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2"]
