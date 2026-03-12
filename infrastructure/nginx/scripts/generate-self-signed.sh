#!/usr/bin/env bash
set -euo pipefail

# Generates a self-signed cert for IP-based HTTPS.
# Output:
#   infrastructure/nginx/certs/server.key
#   infrastructure/nginx/certs/server.crt
#
# Usage:
#   ./infrastructure/nginx/scripts/generate-self-signed.sh
#

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CERT_DIR="$REPO_ROOT/infrastructure/nginx/certs"
IP="163.245.222.46"

mkdir -p "$CERT_DIR"

openssl req -x509 -newkey rsa:2048 \
  -sha256 -days 3650 -nodes \
  -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.crt" \
  -subj "/CN=$IP" \
  -addext "subjectAltName=IP:$IP"

echo "Wrote:"
echo "  $CERT_DIR/server.key"
echo "  $CERT_DIR/server.crt"

