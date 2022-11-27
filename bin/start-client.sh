#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

if [ -f .env ]; then
  export $(grep '^SND_SERVER_' .env | xargs)
fi

npm run client:dev
