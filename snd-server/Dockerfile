FROM python:3.10-slim-bullseye

WORKDIR /snd-server

RUN pip install poetry

COPY ./pyproject.toml /snd-server/
COPY ./poetry.toml /snd-server/
COPY ./poetry.lock /snd-server/
RUN poetry install


COPY ./snd-server /snd-server


EXPOSE 6660
