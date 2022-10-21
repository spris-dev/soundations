#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

docker compose build
docker save soundations-snd-server > ./soundations-snd-server.image

ssh-add - <<< "${SND_MAIN_SERVER_KEY}"

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker load < ./soundations-snd-server.image
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker compose up -d --remove-orphans

DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker container prune -f
DOCKER_HOST="ssh://${SND_MAIN_SERVER_HOST}" docker image prune -f
