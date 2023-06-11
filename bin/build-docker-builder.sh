#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

DOCKER_BUILDKIT=1 docker build \
  -t snd-builder \
  -f Dockerfile.builder \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  .
