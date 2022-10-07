#!/usr/bin/env bash

set -euo pipefail

export $(grep -v '^#' $1 | xargs)
