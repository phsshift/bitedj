# Ubuntu Touch ARM64 test package

Build from the repository root:

```sh
clickable build --config packaging/ubuntu-touch/clickable.yaml --arch arm64
python3 scripts/verify-ut-click.py build reports-ut
```

The Actions `ubuntu-touch-click` job performs this in a pinned native ARM64
Clickable Noble SDK. The 24.04-1.x SDK supplies stable Qt5; the Click targets
24.04-2.x, which shares its base OS/Qt5 ABI. Clickable CLI is pinned to 8.10.0.
The phone's experimental Qt6 stack is not used by this target.

The build compiles the actual application and engine with
`QT6=OFF, BITEDJ_UBUNTU_TOUCH=ON`, runs upstream unit tests, installs all
application resources, bundles non-framework audio/codec dependencies, then
builds and reviews the Click. Framework Qt, platform plugins, graphics drivers
and the C/C++ runtime remain supplied by Ubuntu Touch. The post-package audit
checks the extracted files, AArch64 ELF, source commit, permissions and SHA256.
Qt6 native screenshot tests remain mandatory in their existing separate job;
producing a target test package does not imply these have passed.

Mobile mode uses Lomiri/Maliit for input. It refuses appliance shutdown,
Sway rotation, direct unmount and appliance log-export commands. It does not
stop decks or recordings when an unsupported system eject is requested.
The desktop entry requests landscape orientation.

For the initial device test, the application exposes ALSA `default` and `pulse`
and selects `default` on first launch. An app-local ALSA configuration bridges
PortAudio to the existing PulseAudio server; the launcher changes no system
ALSA file, default sink or service. Its AppArmor policy requests audio,
keeping the display awake. Test audio must be placed in the app's private data
folder; the reserved music_files_read permission is not requested. Direct access
to the shared Music folder awaits a supported import path. USB audio/MIDI device
permissions are deliberately outside this first system-audio test package.
MOTU testing is deferred until successful GUI and built-in sound tests.

Logs: `~/.local/share/bitedj.phsshift/launch.log` (or the corresponding XDG data
location). Settings: `~/.config/bitedj.phsshift/`. Runtime GUI, scaling, waveforms,
physical playback, multi-touch, underruns and restart persistence remain
NOT TESTED until the package is installed and exercised on merlin.

Do not install a partial download, a package with failed target unit tests, or
the native Ubuntu runner tarball. Do not present a CI-only package as a release.

References:
- https://forums.ubports.com/topic/12474/changes-in-ubuntu-touch-24.04-2.0-for-app-developers
- https://clickable-ut.dev/en/latest/project-config.html
