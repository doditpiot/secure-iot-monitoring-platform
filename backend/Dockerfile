# Backend Docker image
# Author: HAMAILI Ahmed-Imad

FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies first so Docker can reuse this layer when only the
# application code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Uvicorn serves the FastAPI application inside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
