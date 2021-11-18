FROM python:3.10-slim as stage0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update ; \
    apt-get install -y --no-install-recommends \
        gcc \
        g++

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /code/app

EXPOSE 8080

WORKDIR /code

# --------------- unit tests --------------

FROM stage0 as test
RUN pip install pytest==6.2.5 pytest-asyncio==0.15.1

RUN python3 -m pytest tests

# ------------ final -----------------------

FROM stage0 as final

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
