FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY sql/ ./sql/
COPY models/ ./models/
COPY dbt_project.yml .

CMD ["python", "-m", "src.run_pipeline"]
