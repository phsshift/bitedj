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

SDK/mobile implementation commit: 894d8bf4d3636a9ba4fa7f4441d74d1ded341feb. Branch push requested; run status not polled. Await user notification before inspecting CI.

Run 42080627840: SDK job failed at Clickable argument parsing before image setup/compilation. Nine packaging checks passed on runner. Fix moves build before --config/--arch. Native job was compiling at explicit user status check; no final result inferred.
Clickable invocation fix pushed: 1547af3d57e18e5e8242586b2932bd759a711709. Push trigger requested; no automatic monitoring.

Explicit user result check: run 42081642183 completed with failure at 1547af3.
Native application/tests compiled; unit test step and staging/audit passed;
all 11 visual tests still failed. SDK packaging checks: 9 passed. Clickable
argument parsing now succeeds and pinned SDK image downloads, but image setup
fails before compilation: generated image tag appends a UUID to the sha256
digest reference, producing "invalid reference format" (exit 125/2).
No Click produced or phone installation/launch attempted. Next repair should
preserve digest pinning while giving Clickable a valid local image tag.
Run: https://github.com/phsshift/bitedj/actions/runs/42081642183

## Build repair — 2026-11-06
Recovered original master prompt and current restrictions. Successful BiteDJ
build precedes all further MOTU checks. No phone audio/system changes.
Phone memory snapshot: 3747 MiB RAM, 1683 MiB available, 1469 MiB swap used.
Keep compilation/SDK work on GitHub-hosted ARM64; local work is lightweight.
No specific numeric user memory cap was found in the saved original prompt.

Pushed f03b68eb80116d99f117d2141dba52effd6868d8 to ubuntu-touch-merlin.
Workflow pulls the configured pinned SDK digest, assigns a digest-derived
local tag, verifies identical image IDs, saves provenance, then overrides
CLICKABLE_DOCKER_IMAGE. Clickable can append its dependency-image UUID to
this valid tag without corrupting the immutable digest reference.
PASS: 9 packaging/launcher tests, workflow YAML parsing, SDK shell syntax.
NOT TESTED: new SDK compilation/package, new visual results, phone runtime.
Strict visual tests/goldens remain unchanged. Prior run has 11 failures;
text-colour checks now pass in several cases, but screenshots still differ
and harmonic_match_drive reports no visible track table. Investigate those
diagnostics; do not weaken comparisons to obtain a green run.
Push requests the next Actions build. Per explicit no-automatic-polling rule,
await user email notification or explicit check before querying new CI status.
Successful build is not yet established. No package installed or launched.

## Continued build repairs — 2026-11-06
Explicit user check: run 42187255697 failed. Native compilation/unit tests
and staging/audit passed; visual tests failed. SDK preparation succeeded,
but Clickable preferred Podman while the alias existed only in Docker.
Pushed ff45b1d83b26f55eddf4d12f521a432c07555325: job-wide
CLICKABLE_DOCKER_COMMAND=docker selects the same image store throughout.
Verified selection against the published Clickable 8.10.0 wheel source.

Downloaded only 3.25 MB diagnostic artifact 13488751584, verified SHA256
ce3028cfb4a22993d909f998beab43b3bab2806c16bf2e887307be9add53988a
and all ZIP member CRCs; extracted to diagnostics/run7. No large binary download.
Actual screenshots show absent quantize artwork and a Settings/Devices page
where harmonic_match_drive expects Browse. The controller startup watchdog
runs after 1500 ms and can overwrite scenario navigation.
Pushed 43c5513dfb74b6564f297bd4d3507b8034f56e30: SVG 1.1 xlink image reference.
Pushed 4fed43bb82b9e4a65bcd38c1dcdfe748d71af9bd: bounded visual startup wait
now includes controller startup navigation completion, with a GUI-thread getter.
No golden images, assertion tolerances or test exclusions changed.
PASS: SVG XML/embedded PNG validation, workflow YAML/shell checks, 9 packaging tests.
NOT TESTED until CI: C++ changes, visual comparisons and target SDK build.
Other differences include fonts and initial audio position; do not claim solved.
Git installed in ~/.local/opt/git with ~/.local/bin/git wrapper; system unchanged.
Source snapshot now has an empty Git repository with origin/upstream configured;
remote history NOT fetched. Do not commit all files as a new root accidentally.
No phone audio/VPN/system configuration changes or MOTU tests.

## Automatic monitoring authorized — 2026-11-06 08:48 UTC
User explicitly requests automatic checks and fixes until the build target.
This supersedes the earlier instruction to wait for an email before checking CI.
Continue bounded status checks and repair failures without requesting approval
again. Keep real engine and mandatory tests, compile on ARM64 GitHub runners,
preserve phone memory/system/audio and defer MOTU until successful build.
Latest known run: 42189713679, commit 4fed43bb82b9e4a65bcd38c1dcdfe748d71af9bd.
At this checkpoint GitHub connector transport failed twice; direct public API
also failed with TLS UNEXPECTED_EOF. Current run outcome remains unverified.

## Transport recovery / Qt5 compile repair — 2026-11-06
User explicitly declined VPN changes. Keep VPN entirely untouched.
HTTPS and GitHub connector recovered without configuration changes. Root cause
is unconfirmed; do not attribute the outage to VPN. Project-local read-only
scripts/monitor-bitedj-ci.py retries transient reads four times with bounded
backoff and fresh HTTP connections, then continues bounded monitoring.
Evidence saved in docs/transport-diagnosis.json. This mitigates transient CI
read failures; it does not repair the built-in connector or prove a root cause.
Run 42189713679 SDK image setup now passes and compilation starts. Qt5 compile
fails in legacycontrollersettingsfactory.h due to missing standard headers.
Pushed bed39480cbc63d514420b2d259fde1627f5835ae: replace self-include with
QList, functional, memory and utility. Native job had reached unit tests.
New push schedules replacement run; keep automatic monitoring and repair loop.

## Run 42190826195 / next repair
Run at bed39480cbc63d514420b2d259fde1627f5835ae completed: FAIL.
PASS: native compilation, upstream unit tests, visual environment setup,
native staging/audit, 9 target packaging checks, pinned SDK setup.
FAIL: 11 native visual scenarios (pixel differences), Qt5 compilation.
Previous missing-memory-header failure resolved. Qt5 next rejects
QMutableListIterator<RowInfo> constructed with QVector<RowInfo> at
basesqltablemodel.cpp:879 (Qt6 aliases these containers; Qt5 does not).
Prepared standard erase/remove_if implementation compatible with both.
Prepared separate SDK cache restore/save so failed compilation preserves
bounded compiler cache for the next repair. No tests disabled or weakened.
Startup-navigation repair resolves the prior invisible track table error;
harmonic_match_drive now executes all three screenshot stages and colour checks.
Quantize SVG compatibility changed; compare run11 diagnostics with goldens
before making further visual changes. Successful full build still not achieved.
User requires detailed status each turn, including all job outcomes and next action.
