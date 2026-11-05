# Test results
| Check | Result | Evidence |
|---|---|---|
| Host architecture | PASS | uname: aarch64, merlin kernel |
| Ubuntu Touch channel | PASS | 24.04-2.x/arm64/android9plus/stable, tag 24.04-2.2 |
| ADB connectivity | FAIL | listener creation Operation not permitted |
| MOTU visibility in this session | NOT TESTED | only onboard card in proc; /dev/snd unavailable |
| GitHub account read | PASS | connected account phsshift |
| Existing accessible BiteDJ fork | NOT TESTED | no match in returned account repository list |
| ARM64 compilation / upstream tests | NOT TESTED | no runner started |
| Native audit negative cases | PASS | rejects missing binary and invalid ELF; Python syntax checked |
| Click package / GUI / both decks | NOT TESTED | no build installed |
| Internal / External MOTU separation | NOT TESTED | physical measurement required |
| MIDI / reconnect / underruns | NOT TESTED | no hardware access |
| Pioneer 8ch software / hardware | NOT TESTED | no implementation/test yet |

User's prior successful MOTU ALSA test is accepted; no reconfiguration attempted.
