FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN apt-get update && \
    apt-get install -y  \
    --no-install-recommends curl

COPY ./requirements.txt .
RUN pip install --upgrade pip \
    pip install --no-cache-dir --no-deps \
    -r requirements.txt

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --reload --port 8000