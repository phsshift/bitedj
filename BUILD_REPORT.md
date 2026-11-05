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
