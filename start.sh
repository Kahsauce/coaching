#!/bin/sh
# Lance à la fois le backend FastAPI et le frontend React
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

start_backend() {
    (cd "$SCRIPT_DIR/packages/api" && ./start.sh "$@")
}

start_frontend() {
    (cd "$SCRIPT_DIR/apps/web" && npm install && npm start)
}

start_backend &
BACKEND_PID=$!

start_frontend &
FRONTEND_PID=$!

trap 'kill $BACKEND_PID $FRONTEND_PID 2>/dev/null' INT TERM EXIT
wait $BACKEND_PID $FRONTEND_PID
