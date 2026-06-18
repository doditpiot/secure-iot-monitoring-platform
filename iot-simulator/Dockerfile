# IoT simulator Docker image
# Author: HAMAILI Ahmed-Imad

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulator.py .
COPY devices.json .

# The simulator runs forever and publishes MQTT telemetry every few seconds.
CMD ["python", "simulator.py"]
