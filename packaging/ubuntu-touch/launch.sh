#!/bin/sh
set -eu
# Click confinement permits packaged executables, not system coreutils.
case "$0" in
    */*) launcher_dir=${0%/*} ;;
    *) launcher_dir=. ;;
esac
app_root=$(CDPATH= cd -- "$launcher_dir" && pwd)
app_config="${XDG_CONFIG_HOME:-$HOME/.config}/bitedj.phsshift"
app_data="${XDG_DATA_HOME:-$HOME/.local/share}/bitedj.phsshift"
"$app_root/usr/bin/mkdir" -p "$app_config" "$app_data"
export LD_LIBRARY_PATH="$app_root/lib/aarch64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export ALSA_CONFIG_PATH="$app_root/alsa.conf"
export ALSA_PLUGIN_DIR="$app_root/lib/aarch64-linux-gnu/alsa-lib"
export FONTCONFIG_FILE="$app_root/fonts.conf"
export QT_QPA_PLATFORM=ubuntumirclient
export QT_IM_MODULE=maliit
# Temporary opt-in diagnostics for the silent mobile Master investigation.
export BITEDJ_AUDIO_DIAGNOSTICS=1
# Preserve the shell's display scale and session audio server.
exec "$app_root/usr/bin/mixxx" --settings-path "$app_config" \
    --resource-path "$app_root/usr/share/mixxx" --full-screen "$@" >> "$app_data/launch.log" 2>&1
