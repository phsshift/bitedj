#!/usr/bin/env bash
# Disposable GitHub-hosted runner only. Never run buildenv/setup on merlin.
set -euo pipefail
if [[ "${GITHUB_ACTIONS:-}" != true || "${RUNNER_ENVIRONMENT:-}" != github-hosted || -z "${RUNNER_TEMP:-}" || -z "${GITHUB_WORKSPACE:-}" || -z "${GITHUB_ENV:-}" ]]; then
    echo 'Refusing visual-test setup outside a GitHub-hosted runner.' >&2
    exit 2
fi
mkdir -p reports
sudo apt-get update
sudo apt-get install -y --no-install-recommends pulseaudio pulseaudio-utils libasound2-plugins alsa-utils fonts-noto-cjk fonts-inter apparmor

# Canonical's per-executable userns allowance, not a global sysctl change:
# https://documentation.ubuntu.com/release-notes/24.04/
visual_binary="$(realpath build/bitedj-visual-test)"
profile_file="${RUNNER_TEMP}/bitedj-visual.apparmor"
cat > "$profile_file" <<EOF
abi <abi/4.0>,
include <tunables/global>
profile bitedj-ci-visual "$visual_binary" flags=(unconfined) {
    userns,
}
EOF
if [[ -r /sys/module/apparmor/parameters/enabled ]] && [[ "$(cat /sys/module/apparmor/parameters/enabled)" == Y ]]; then
    sudo apparmor_parser -r "$profile_file"
fi
# --help still performs the harness namespace/mount setup, before Qt starts.
"$visual_binary" --help > reports/visual-namespace-probe.log 2>&1

# The screenshot harness opens an actual PortAudio/ALSA output. Supply a
# clocked virtual sink so the no-device banner does not replace the tabs.
export XDG_RUNTIME_DIR="${RUNNER_TEMP}/bitedj-visual-runtime"
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
pulseaudio --daemonize=yes --exit-idle-time=-1 --log-target="file:${GITHUB_WORKSPACE}/reports/pulseaudio.log"
export PULSE_SERVER="unix:${XDG_RUNTIME_DIR}/pulse/native"
pactl load-module module-null-sink sink_name=merlin_ci channels=2 rate=48000 > reports/pulse-module.txt
pactl set-default-sink merlin_ci
export ALSA_CONFIG_PATH="${RUNNER_TEMP}/bitedj-visual-alsa.conf"
cat > "$ALSA_CONFIG_PATH" <<'EOF'
</usr/share/alsa/alsa.conf>
pcm.!default { type pulse }
ctl.!default { type pulse }
EOF
pactl info > reports/pulse-info.txt
pactl list short sinks > reports/pulse-sinks.txt
aplay -L > reports/alsa-devices.txt
# A bounded silence write verifies the ALSA -> PulseAudio path, without
# opening any physical output. The default sink above is explicitly virtual.
python3 - <<'PY'
import subprocess
subprocess.run(['aplay', '-q', '-D', 'default', '-t', 'raw', '-f', 'S16_LE',
                '-r', '48000', '-c', '2'], input=bytes(4800 * 4), check=True, timeout=15)
PY
# The skin explicitly requests Inter. Avoid host-dependent fallback fonts and
# RGB subpixel fringes in offscreen pixel/text-colour assertions.
export FONTCONFIG_FILE="${RUNNER_TEMP}/bitedj-visual-fonts.conf"
cat > "$FONTCONFIG_FILE" <<'EOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <include ignore_missing="no">/etc/fonts/fonts.conf</include>
  <match target="font">
    <edit name="rgba" mode="assign"><const>none</const></edit>
  </match>
</fontconfig>
EOF
fc-match -f '%{family}\n' Inter > reports/inter-font-match.txt
python3 - <<'PYFONT'
from pathlib import Path
families = Path('reports/inter-font-match.txt').read_text().strip().split(',')
if 'Inter' not in (family.strip() for family in families):
    raise SystemExit('Inter font missing: refusing silent font fallback')
PYFONT
fc-match -v Inter > reports/inter-font-properties.txt
fc-list > reports/fonts.txt
{
    echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
    echo "PULSE_SERVER=$PULSE_SERVER"
    echo "ALSA_CONFIG_PATH=$ALSA_CONFIG_PATH"
    echo "FONTCONFIG_FILE=$FONTCONFIG_FILE"
} >> "$GITHUB_ENV"
