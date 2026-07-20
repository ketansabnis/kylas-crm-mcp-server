#!/usr/bin/env bash
#
# Smoke-test a deployed Kylas MCP endpoint WITHOUT any MCP client.
# Runs the MCP initialize handshake, lists tools, and calls get_current_user
# (which actually hits the Kylas API, proving the x-api-key path works).
#
# Usage:
#   MCP_URL="https://<id>.lambda-url.<region>.on.aws/mcp" \
#   KYLAS_KEY="<your kylas api key>" \
#   ./deploy/smoke-test.sh
#
set -euo pipefail

MCP_URL="${MCP_URL:?set MCP_URL to the /mcp endpoint}"
KYLAS_KEY="${KYLAS_KEY:?set KYLAS_KEY to your Kylas API key}"

hdr=(-H "Content-Type: application/json"
     -H "Accept: application/json, text/event-stream"
     -H "x-api-key: ${KYLAS_KEY}")

echo "==> 1) initialize"
curl -s -w "\n[HTTP %{http_code}]\n" -X POST "$MCP_URL" "${hdr[@]}" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}' \
  | sed 's/^data: //' | head -c 500
echo; echo

echo "==> 2) tools/list (count only)"
curl -s -X POST "$MCP_URL" "${hdr[@]}" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | sed 's/^data: //' | grep -o '"name"' | wc -l | xargs echo "tools returned:"
echo

echo "==> 3) tools/call get_current_user (hits Kylas API)"
curl -s -w "\n[HTTP %{http_code}]\n" -X POST "$MCP_URL" "${hdr[@]}" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_current_user","arguments":{}}}' \
  | sed 's/^data: //' | head -c 800
echo
