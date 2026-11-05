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

Latest completed run: https://github.com/phsshift/bitedj/actions/runs/42041134577
Commit: 6bd00bf299aa88e000fbc4f396751edabec30604.
PASS: compilation, virtual audio, namespace probe, native runner staging/audit,
compiler cache; 1154 unit tests passed, 0 failed (13 disabled, 47 skipped).
FAIL: 11 visual scenarios. Native artifact exists on GitHub but local download was
truncated and FAILED SHA256; no binary used. Recovered CRC-checked diagnostic
members for analysis only. Evidence: docs/ci-run-3.json and BUILD_REPORT.md.

Next action: await the user's email notification after the font/render repair
is pushed, then inspect that run. Do not poll automatically.
Repair adds/verifies Inter (required by skin, missing in runner), process-only
Fontconfig rgba=none, failed text-colour cell/window/crop evidence and separate
small diagnostics/large native artifacts. No golden, tolerance or assertion changed.
Remaining failures include stopped position -30.00 vs golden -30.11, blank quantize
icons and text-colour samples; do not claim fonts explain/fix every mismatch.
Local shell/YAML/phone-refusal checks PASS. New C++ diagnostics and visual result
await CI. Read current commit from branch head or reports/commit.txt.
Current session is unrestricted; initial sandbox findings above are historical.
No phone audio/system/VPN changes. Never run CI setup on the phone.

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

## Resume audit — 2026-11-05
See diagnostics/run3/RESUME_FINDINGS.md. Saved run3 reports now establish unit and visual setup success, with visual comparisons still failing. Full archive SHA256 remains unverified. No Actions polling or phone launch performed.

## Next stage: Ubuntu Touch SDK / system audio first
Prepared from f16370a493332a6a2f50be6d7f28bd238a5ac94e. Full local source snapshot:
/home/phablet/Documents/Codex/bitedj-f16370a493332a6a2f50be6d7f28bd238a5ac94e.
See packaging/ubuntu-touch/README.md. Mobile compile flag gates appliance system
actions and uses system audio. Qt5 touch compatibility and a pinned SDK Click
build/audit job are prepared. 9 local package/launcher checks PASS; C++/SDK/GUI
NOT TESTED. Native Qt6 visual tests still mandatory, with original goldens.
User wants GUI + built-in system audio verified before connecting MOTU.
Continue respecting the user's no-automatic-polling request: await their build
completion email or explicit result-check request, then inspect diagnostics.
Do not infer runtime compatibility from compilation or ELF architecture alone.
