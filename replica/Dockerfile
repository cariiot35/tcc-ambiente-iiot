FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir paho-mqtt psutil

COPY gemeo_digital.py .

CMD ["python", "-u", "gemeo_digital.py"]
