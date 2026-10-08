#!/bin/bash
# Launch the live restream in the background and tail the log.
# Reads .env manually (line-by-line) to safely handle & in values.
set -uo pipefail

LOG=live.log
: > "$LOG"

if [[ -f .env ]]; then
  set -a
  while IFS= read -r line; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$line" ]] && continue
    [[ "$line" == *=* ]] && export "$line"
  done < .env
  set +a
fi

nohup bash restream.sh > "$LOG" 2>&1 &
PID=$!
echo "Started restream (PID=$PID). Log: $LOG"
echo "Waiting 15s for connection to settle..."
sleep 15
echo "===== LOG SO FAR ====="
tail -40 "$LOG"
