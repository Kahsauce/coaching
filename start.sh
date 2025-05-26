#!/bin/sh
# Wrapper to launch the API from the repository root
set -e
cd "$(dirname "$0")/packages/api"
exec ./start.sh "$@"
