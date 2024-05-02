FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=fhir_transformer
ENV POSTGRES_USER=ccharles
ENV POSTGRES_PASSWORD=fhir_password


CMD ["python", "/app/src/fhir_transformers.py"]