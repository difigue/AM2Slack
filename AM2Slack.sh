#!/bin/bash

set -a
source .env
set +a

if ! [[ "$EXECUTION_INTERVAL" =~ ^[0-9]+$ ]]; then
  echo "Warning: EXECUTION_INTERVAL is not set in .env file or is not a valid integer. Setting to 60 seconds." >&2
  EXECUTION_INTERVAL=60
fi

if [[ -z "$PROGRAM_DIR" ]]; then
  echo "Error: PROGRAM_DIR is not set in .env file." >&2
  exit 1
fi

watch -n "$EXECUTION_INTERVAL" python3 "$PROGRAM_DIR"