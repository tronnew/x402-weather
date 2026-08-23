# Deployment Guide

## Quick Start

```bash
# Clone
git clone https://github.com/tronnew/x402-weather.git
cd x402-weather

# Install dependencies
pip install -e .

# Run
python x402_server.py
```

## Production (Docker)

```bash
cd docker
docker-compose up -d
```

## Production (Systemd)

```bash
sudo cp x402-weather.service /etc/systemd/system/
sudo systemctl enable x402-weather
sudo systemctl start x402-weather
```

## Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name forex2026.mooo.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
