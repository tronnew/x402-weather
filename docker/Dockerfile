FROM python:3.11-slim

WORKDIR /app
RUN pip install flask gunicorn requests eth-account web3

COPY server.py .
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "server:app"]
