#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

export FASTAPI_ENV=production


mkdir -p "$(dirname "${SND_SQLITE_DB_PATH}")"

cd ./snd-server && \
  poetry run uvicorn main:app --host $SND_SERVER_HOST --port $SND_SERVER_PORT
