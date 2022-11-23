#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

poetry --version
poetry install
