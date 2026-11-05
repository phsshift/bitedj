# Test results
| Check | Result | Evidence |
|---|---|---|
| Host architecture | PASS | uname: aarch64, merlin kernel |
| Ubuntu Touch channel | PASS | 24.04-2.x/arm64/android9plus/stable, tag 24.04-2.2 |
| ADB connectivity | FAIL | listener creation Operation not permitted |
| MOTU visibility in this session | NOT TESTED | only onboard card in proc; /dev/snd unavailable |
| GitHub account read | PASS | connected account phsshift |
| Existing accessible BiteDJ fork | PASS | phsshift/bitedj, ubuntu-touch-merlin |
| ARM64 compilation | PASS | run 42020298377, application and mixxx-test built |
| Unit tests, third run | PASS | 1154 passed, 0 failed, 13 disabled, 47 skipped; run 42041134577 |
| Visual tests, third run | FAIL | 11 scenarios fail pixel/text comparisons |
| Corrected MP3 reference and visual executable compilation | PASS | run 42033227856 |
| Visual runner audio/namespace setup | PASS | run 42041134577; no-audio banner removed, namespace probe passed |
| Native runner install audit | PASS | AArch64 ELF, runner libraries, skin; target runtime NOT TESTED |
| Third-run artifact local SHA256 | FAIL | truncated download; native binary not used |
| Font/render repair | NOT TESTED | Inter absent in captured font list; new CI validation required |
| Native audit negative cases | PASS | rejects missing binary and invalid ELF; Python syntax checked |
| Click package / GUI / both decks | NOT TESTED | no build installed |
| Internal / External MOTU separation | NOT TESTED | physical measurement required |
| MIDI / reconnect / underruns | NOT TESTED | no hardware access |
| Pioneer 8ch software / hardware | NOT TESTED | no implementation/test yet |

User's prior successful MOTU ALSA test is accepted; no reconfiguration attempted.

## Ubuntu Touch target preparation
PASS locally: 9 packaging/launcher regression checks; shell syntax;
refusal of SDK build script on the phone. Target C++ compilation, upstream
unit suite in SDK, Clickable review, installation, GUI and system sound remain
NOT TESTED pending CI and device testing. MOTU deferred by user.
