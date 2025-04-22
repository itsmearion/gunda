#!/bin/bash

LOG_FILE="/var/log/syslog"
PATTERN="msg_id is too low"

if grep -q "$PATTERN" "$LOG_FILE"; then
    echo "[AUTO-HEAL] Detected msg_id sync issue. Healing..."
    chronyc -a makestep
    systemctl restart gundabot
    echo "[AUTO-HEAL] Bot restarted & time resynced."
fi