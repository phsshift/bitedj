#!/usr/bin/env bash
# Invoked by Clickable inside the pinned SDK, never directly on the phone.
set -euo pipefail
source_root=$(realpath "$1")
build_root=$(realpath -m "$2")
install_root=$(realpath -m "$3")
if [[ ! -f /.dockerenv || $(uname -m) != aarch64 || -d /android ]]; then
    echo 'Refusing target build outside the ARM64 SDK container.' >&2
    exit 2
fi
reports="$source_root/reports-ut"
mkdir -p "$reports"
exec > >(tee "$reports/sdk-build.log") 2>&1
uname -a > "$reports/runner.txt"
dpkg-query -W > "$reports/packages.txt"
git -C "$source_root" rev-parse HEAD > "$reports/commit.txt"
ccache --max-size=2G
cmake -S "$source_root" -B "$build_root" \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DQT6=OFF -DBITEDJ_UBUNTU_TOUCH=ON \
    -DBUILD_TESTING=ON -DBUILD_BENCH=OFF -DDOWNLOAD_MANUAL=OFF \
    -DINSTALL_USER_UDEV_RULES=OFF -DWARNINGS_FATAL=OFF -DCMAKE_INSTALL_PREFIX=/usr
cmake --build "$build_root" --target mixxx mixxx-test --parallel 2
QT_QPA_PLATFORM=offscreen ctest --test-dir "$build_root" -LE visual \
    --no-tests=error --timeout 120 --parallel 1 --output-on-failure \
    --output-junit "$reports/unit-tests.xml"
DESTDIR="$install_root" cmake --install "$build_root" --prefix /usr
python3 "$source_root/scripts/stage-ut-runtime.py" "$source_root" "$install_root" "$reports"
