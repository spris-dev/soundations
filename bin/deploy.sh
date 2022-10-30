#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

export COMPOSE_PROJECT_NAME=soundations

IMAGE_TAR_PATH=/tmp/soundations-images.tar.gz
IMAGE_NAMES=(
  "soundations-snd-server"
  "soundations-snd-proxy"
)

docker compose build
docker save "${IMAGE_NAMES[@]}" | gzip > $IMAGE_TAR_PATH

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker load < $IMAGE_TAR_PATH
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose up -d --remove-orphans

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose ps
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose logs

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker container prune -f
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker image prune -f
