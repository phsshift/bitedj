# Test.20 phone startup failure

Installed package: 0.1.0-test.20, source cb8fbf13112758b193b3696f573493570a0ab84d.
Installation PASS; launcher helper permissions fixed; application startup FAIL.

The launcher creates app-private directories and executes mixxx. The dynamic
loader aborts before main with missing QOpenGLFunctions_2_1 Qt_5 symbols.
Read-only ldd -r confirms five unresolved references. Normal ldd only resolves
library names and did not detect this ABI variant mismatch.

Phone: libqt5gui5-gles 5.15.13+dfsg-1. SDK before repair: libqt5gui5t64,
qtbase5-dev and libqt5opengl5-dev 5.15.13+dfsg-1ubuntu1 (desktop OpenGL).

Repair: select qtbase5-gles-dev and libqt5quick5-gles in SDK dependencies,
remove desktop-only Qt5 OpenGL module from mobile CMake components, link GLESv2,
require the Qt GLES header configuration, reject desktop Qt OpenGL function
symbols during staging. Native desktop build keeps its original configuration.
Upstream waveform sources already guard legacy desktop renderers with
QT_OPENGL_ES_2; retain the GLES shader renderer and full audio engine.

Reference: https://packages.ubuntu.com/noble/qtbase5-gles-dev

Local packaging checks: 11 PASS. New C++/SDK build: NOT TESTED until CI runs.
Do not install desktop Qt over the phone's existing framework or modify audio.
GUI, playback and MOTU: NOT TESTED. Native visual failures remain unresolved.
