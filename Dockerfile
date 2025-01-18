FROM python:3.12.3-slim-bookworm as pip_requirements

COPY ./pyproject.toml ./poetry.lock /
RUN pip install poetry==1.8.0 \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev

FROM python:3.12.3-slim-bookworm

WORKDIR /app/worklog
COPY ./src/worklog /app/worklog
COPY --from=pip_requirements /requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENTRYPOINT ["fastapi"]
CMD ["run", "main.py", "--port", "80"]
