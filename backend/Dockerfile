FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-jose pandas

CMD ["sh", "-c", "python wait_for_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]