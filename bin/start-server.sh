#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

. ./bin/set-env.sh

cd ./snd-server && \
  poetry run uvicorn main:app --reload --host $SND_SERVER_HOST --port $SND_SERVER_PORT
