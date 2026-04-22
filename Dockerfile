FROM python:3.11.15-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.3.4"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY fastapi-test .

CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000"]