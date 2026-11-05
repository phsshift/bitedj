# Handoff — 2026-11-05
Current upstream SHA: 87f46b4bf176811a707d05e1806392d2c8de8d83.
Local commit: none (git unavailable; this is an overlay).
First Actions run: https://github.com/phsshift/bitedj/actions/runs/42020298377 (completed: failure in tests; compilation PASS).
Last successful Actions run: none.
Integration commit: 5f66e31f65e61eb0fd29d7bdce432f56ce0b89d5.
Last installed version: not inspected; no installation attempted.
Stages A/B/C/D/E: incomplete.

Environment runs on merlin itself in a restricted session. No direct shell network DNS,
git/gh/cmake/compiler, ADB listener permission or /dev/snd visibility.
GitHub connector can read repositories and create commits/branches in existing repos;
it cannot create forks. Fork verified: https://github.com/phsshift/bitedj, parent TeamDeckshark/bitedj.
Branch ubuntu-touch-merlin created at pinned upstream SHA.

Latest completed run: https://github.com/phsshift/bitedj/actions/runs/42033227856
Commit b3e5de9db232f27ecbf249c6a0941b452f4fd62a: compilation and MP3 fix PASS;
1154 tests PASS, 11 visual FAIL, 13 disabled, 47 skipped. No installation artifact
was staged. Artifact diagnostics downloaded with SHA256 verified; see docs/ci-run-2.json.

Next action: await the user's email notification after the visual-environment
repair is pushed, then inspect that run. Do not automatically poll or monitor.
Repair adds runner-only virtual PulseAudio/ALSA output, CJK fonts, a named AppArmor
profile for the visual executable, and fail-closed namespace setup in the harness.
No goldens/tolerances changed. Additional render differences remain NOT TESTED.
Native staging now runs after compilation even if tests fail, explicitly recording
test outcomes; its archive is diagnostic and must not be treated as a release.
Compiler cache is preserved on test failure to reduce repeat work.
Current source commit can be read from branch head/CI reports/commit.txt.
Local syntax/YAML/host-refusal checks PASS; full changes await CI compilation.
Current session is unrestricted; earlier sandbox findings above are historical.
No phone audio/system/VPN modifications made. Do not run CI setup on the phone.

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
