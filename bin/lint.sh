#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

. ./bin/set-env.sh

poetry run black --check snd-server
poetry run pyright snd-server