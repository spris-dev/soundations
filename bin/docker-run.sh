#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

. ./bin/set-env.sh

docker run \
  --rm \
  --mount "type=bind,src=$(pwd),dst=/soundations" \
  -w /soundations \
  snd-builder \
  "$@"
