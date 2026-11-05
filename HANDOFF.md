# Handoff — 2026-11-05
Current upstream SHA: 87f46b4bf176811a707d05e1806392d2c8de8d83.
Local commit: none (git unavailable; this is an overlay).
Last successful Actions run: none.
Last installed version: not inspected; no installation attempted.
Stages A/B/C/D/E: incomplete.

Environment runs on merlin itself in a restricted session. No direct shell network DNS,
git/gh/cmake/compiler, ADB listener permission or /dev/snd visibility.
GitHub connector can read repositories and create commits/branches in existing repos;
it cannot create forks. Fork verified: https://github.com/phsshift/bitedj, parent TeamDeckshark/bitedj.
Branch ubuntu-touch-merlin created at pinned upstream SHA.

Next action: upload integration files through GitHub tree/commit/ref APIs and monitor
first Actions build. See branch history for integration commit SHA. Preserve upstream remote when a real git checkout becomes available.
Check buildenv apt failures; avoid declaring workflow operational before actual run.

Before phone launch: gate poweroff, swaymsg rotation, umount and kiosk OSK supervisor
operations under a target-specific platform mode; inspect all other process calls.
No launch permitted by this checkpoint until the hardware-specific operations are reviewed.
Native workflow must evolve into Clickable SDK build; never infer ABI from aarch64 alone.
Determine Qt platform plugin and sandbox audio/MIDI access from real target packages.
Do not change global AppArmor, ALSA, kernel, VPN or system partition.

Resume reads:
  cat /home/phablet/Documents/Codex/bitedj-merlin/HANDOFF.md
  cat /home/phablet/Documents/Codex/bitedj-merlin/UPSTREAM_SHA
No rollback required: no phone app/settings/system configuration changed.
