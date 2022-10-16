#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

. ./bin/set-env.sh

DOCKER_BUILDKIT=1 docker build \
  -t snd-builder \
  .
