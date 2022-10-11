FROM python:3.10-slim-bullseye

WORKDIR /snd-server


COPY ./snd-server/requirements.txt /snd-server/
RUN pip install -r requirements.txt


COPY ./snd-server /snd-server


EXPOSE 6660
