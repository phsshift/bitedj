# BiteDJ on Ubuntu Touch merlin — bootstrap checkpoint
Status: NOT BUILT / NOT INSTALLED.
Upstream: https://github.com/TeamDeckshark/bitedj
Pinned upstream: 87f46b4bf176811a707d05e1806392d2c8de8d83 (Mixxx base 2.5.6).

Development fork: https://github.com/phsshift/bitedj, branch ubuntu-touch-merlin.
The local bitedj-merlin folder holds integration files and reference snapshots only;
GitHub holds the complete application sources. Preserve upstream remote in git checkouts.

The initial workflow builds the real application and upstream tests on ubuntu-24.04-arm.
It stages a native Linux installation, checks AArch64 ELF, runner ldd resolution and skin.
It does not yet produce Click, bundle a runtime, or demonstrate Ubuntu Touch compatibility.
Never install its native tarball as if it were a verified Click.

Do not run upstream buildenv on the phone. It is intended exclusively for CI.
Do not launch unmodified appliance code on the phone: it contains poweroff and umount.
See HANDOFF.md for the next action.
