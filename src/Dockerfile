FROM python:3.9-slim as stage0

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install fastapi==0.68.1 uvicorn==0.15.0 SQLAlchemy==1.4.25 asyncpg==0.24.0

EXPOSE 8080

COPY . /app

WORKDIR /app

# --------------- unit tests --------------

FROM stage0 as test
RUN pip install pytest==6.2.5 pytest-asyncio==0.15.1

RUN python3 -m pytest tests

# ------------ final -----------------------

FROM stage0 as final

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
