#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

. ./bin/set-env.sh

docker run \
  --rm \
  -v $(pwd):/soundations \
  -w /soundations \
  snd-builder \
  "$@"
