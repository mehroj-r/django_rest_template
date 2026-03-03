#!/bin/sh
set -e

echo "[$(date)] Running healthcheck..."

if curl http://localhost:8000/api/v1/health/ > /dev/null; then
  echo "Django healthcheck passed ✅"
  exit 0
else
  echo "Django healthcheck failed ❌"
  exit 1
fi
