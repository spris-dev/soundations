#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

IMAGE_TAR_PATH=/tmp/soundations-snd-server.image.gz

docker compose build
docker save soundations-snd-server | gzip > $IMAGE_TAR_PATH

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker load < $IMAGE_TAR_PATH
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose up -d --remove-orphans

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose ps
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose logs

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker container prune -f
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker image prune -f
