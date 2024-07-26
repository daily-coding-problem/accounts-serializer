FROM python:3.12.0-alpine3.17

WORKDIR /app

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi \
    && apk del .build-deps

ENTRYPOINT ["python", "accounts_serializer.py"]

CMD ["--help"]
