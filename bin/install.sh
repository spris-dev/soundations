#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

./bin/install-python-deps.sh
./bin/install-node-deps.sh
