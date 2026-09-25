#!/usr/bin/env bash
# Keeps Azia running 24/7: if the bot crashes or the internet drops,
# it restarts automatically after 5 seconds.
#   chmod +x run.sh && ./run.sh
# Stop with Ctrl+C twice.

cd "$(dirname "$0")"

[ -f venv/bin/activate ] && source venv/bin/activate

while true; do
    echo "[$(date '+%F %T')] starting Azia" | tee -a azia.log
    python -u main.py 2>&1 | tee -a azia.log
    echo "[$(date '+%F %T')] Azia stopped (exit ${PIPESTATUS[0]}), restarting in 5s..." | tee -a azia.log
    sleep 5
done
