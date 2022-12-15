#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

OPEN_API_PATH=/tmp/soundations-open-api.json
SERVER_API_CLIENT_PATH=./snd-server-api-client

cd ./snd-server && \
  poetry run python ./cli.py generate-open-api --out $OPEN_API_PATH && \
  cd ..

node_modules/.bin/openapi \
  --input $OPEN_API_PATH \
  --output $SERVER_API_CLIENT_PATH \
  --name SoundationsApiClient \
  --client fetch \
  --useOptions \
  --useUnionTypes

rm $OPEN_API_PATH
