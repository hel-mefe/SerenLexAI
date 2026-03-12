#!/usr/bin/env bash
#
# destroy-all.sh — Fully destroy SerenLex backend data (Postgres, MinIO, reports, uploads).
# Use on VPS or local when you want a clean slate. This is DESTRUCTIVE and irreversible.
#
# Usage: ./infrastructure/scripts/destroy-all.sh [--force]
#   --force  Skip confirmation prompt
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$INFRA_DIR"

if [[ "${1:-}" != "--force" ]]; then
  echo "This will:"
  echo "  - Stop and remove all containers (api, ai_worker, postgres, redis, minio)"
  echo "  - Remove all Docker volumes (postgres_data, minio_data, reports_data)"
  echo "  - Delete all files under infrastructure/data/uploads"
  echo ""
  echo "All database data, object storage, reports, and uploads will be PERMANENTLY LOST."
  read -rp "Type 'yes' to continue: " confirm
  if [[ "$confirm" != "yes" ]]; then
    echo "Aborted."
    exit 1
  fi
fi

echo "Stopping and removing containers and volumes..."
docker compose down -v

echo "Cleaning bind-mounted data (uploads)..."
if [[ -d "data/uploads" ]]; then
  find data/uploads -mindepth 1 -delete 2>/dev/null || true
  echo "  Cleared data/uploads"
fi

echo "Done. All backend data has been destroyed. Run 'docker compose up -d' from infrastructure/ for a fresh start."
