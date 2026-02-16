FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements.txt requirements-dev.txt alembic.ini pytest.ini ./
COPY app ./app
COPY tests ./tests
COPY alembic ./alembic

RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
