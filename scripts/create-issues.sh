#!/usr/bin/env bash
# Stellar Wave backlog tool. Dry run by default: validates scripts/wave-issues.json
# and prints totals without any GitHub call. Mutations need an explicit flag:
#   ./scripts/create-issues.sh                  # validate only
#   ./scripts/create-issues.sh --emit out.json  # write rendered issues
#   ./scripts/create-issues.sh --create         # operator: create missing issues
#   ./scripts/create-issues.sh --sync-existing  # operator: restyle linked issues
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$script_dir/wave_issues.py" --repo "${REPO:-Soroban-CII/soroindex}" "$@"
