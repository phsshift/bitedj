# Build report — 2026-11-05

First run: https://github.com/phsshift/bitedj/actions/runs/42020298377
Commit: 5f66e31f65e61eb0fd29d7bdce432f56ce0b89d5

- PASS: dependencies, CMake configuration, native ARM64 application and mixxx-test compilation.
- FAIL: CTest reported 12 failed/not-run tests out of 1212 enabled tests (1225 registered); additional tests were skipped. Do not interpret the remaining count as all passing.
- FAIL: SoundSourceProxyTest.firstSoundTest: cover-test-vbr.mp3 using libmad FPM_DEFAULT returned sample 3326, but test selected 3376. The existing test source documents 3326 for FPM_DEFAULT and links Mixxx #11888 (rounding near silence, not stream offset).
- FAIL: 11 VisualTest scenarios could not run: bitedj-visual-test was registered by CMake but omitted from workflow build targets.
- NOT TESTED: installation staging and native audit (skipped after test failure), Click, target GUI/audio.

Fix: select the documented 3326 reference only for the exact VBR fixture and MAD FPM_DEFAULT provider; preserve all other strict references. Build bitedj-visual-test and retain screenshots/CTest diagnostics. No test excluded or failure ignored.
Validation of fixes: source/workflow review only; awaits next Actions run.
The native runner build does not establish Ubuntu Touch runtime compatibility.

## Second run and visual environment repair
Run: https://github.com/phsshift/bitedj/actions/runs/42033227856
Commit: b3e5de9db232f27ecbf249c6a0941b452f4fd62a.
PASS: ARM64 application, unit and visual executable compilation; corrected MP3 test.
CTest XML: 1154 PASS, 11 FAIL (all visual), 13 disabled, 47 skipped, 1225 registered.
FAIL: drive isolation/mounts denied; missing audio device creates a visible banner;
all screenshot scenarios fail. Reviewed actual/golden beat_grid_lines screenshots.
Additional pixel/text-colour differences remain unproven until the environment rerun.
Artifact ZIP SHA256 verified; summarized evidence in docs/ci-run-2.json.

Repair: add a GitHub-hosted-only setup script providing a clocked PulseAudio null
sink through ALSA, Noto CJK fonts, and a per-executable AppArmor userns allowance
for bitedj-visual-test. No global AppArmor/sysctl change. Make the harness abort
when isolation/identity mapping/tmpfs setup fails, including its --help probe.
This uses the documented Ubuntu 24.04 per-program userns policy:
https://documentation.ubuntu.com/release-notes/24.04/

Split unit/visual reports, keep both mandatory, retain strict golden comparisons.
Attempt native staging after successful compilation even when tests fail, with
validation-status.txt explicitly recording failures; a native archive is diagnostic,
not a release or a phone-compatible package. Save compiler cache even on test failure
to reduce repeated compilation. No Click or hardware success inferred.

Local validation PASS: bash syntax, workflow YAML parsing, setup script refusal
outside GitHub-hosted CI before any mutations. C++ compilation and runtime setup
NOT TESTED locally; next Actions execution is required. No baseline regenerated,
no tolerance increased, and no test failure suppressed.
