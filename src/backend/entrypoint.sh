#!/bin/bash
PUID=${PUID:-1000}
PGID=${PGID:-1000}

XRAY_USER="xray_user"
XRAY_GROUP="xray_group"

function create_user_and_group {
    if ! getent group "$XRAY_GROUP" >/dev/null; then
        groupadd -g "$PGID" "$XRAY_GROUP"
    fi
    if ! id "$XRAY_USER" >/dev/null 2>&1; then
        useradd -u "$PUID" -g "$XRAY_GROUP" -s /bin/bash "$XRAY_USER"
    fi
}

function set_folder_permissions {
    chown -R "$XRAY_USER:$XRAY_GROUP" /xray_base
    chmod -R o+rwx /xray_base/xray_config/xray_core
}

function start_services {
    dbus-daemon --system --fork --nopidfile
    /usr/bin/warp-svc > /dev/null 2>&1 &
    sleep 2
    exec gosu "$XRAY_USER:$XRAY_GROUP" python /xray_base/main.py
}

function main {
    create_user_and_group
    set_folder_permissions
    start_services
}

main
