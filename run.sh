#!/usr/bin/env bash
# Keeps Azia running 24/7: if the bot crashes or the internet drops,
# it restarts automatically after 5 seconds.
#   chmod +x run.sh && ./run.sh
# Stop with Ctrl+C twice.
# If it crashes within 30s of starting 3 times in a row, that's a code or
# config error (not a network blip), so it stops instead of looping forever.

cd "$(dirname "$0")"

[ -f venv/bin/activate ] && source venv/bin/activate

fast_fails=0

while true; do
    echo "[$(date '+%F %T')] starting Azia" | tee -a azia.log
    started=$(date +%s)
    python -u main.py 2>&1 | tee -a azia.log
    code=${PIPESTATUS[0]}

    if [ $(( $(date +%s) - started )) -lt 30 ]; then
        fast_fails=$((fast_fails + 1))
    else
        fast_fails=0
    fi

    if [ "$fast_fails" -ge 3 ]; then
        echo "[$(date '+%F %T')] Azia crashed 3 times right after start. Fix the error above, then run ./run.sh again." | tee -a azia.log
        exit 1
    fi

    echo "[$(date '+%F %T')] Azia stopped (exit $code), restarting in 5s..." | tee -a azia.log
    sleep 5
done
