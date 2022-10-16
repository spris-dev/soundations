#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

pip install poetry
poetry install

./bin/lint.sh
