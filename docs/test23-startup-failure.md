# Test.23 launch diagnosis and next diagnostic build

Installation and phone library relocations PASS. User sees splash only, no main
interface. Normal launch aborts with SIGSEGV about two seconds into initialization.
The prior GLib gdbus-thread fatal and EGL initialization failure do not recur after
process-wide future memory locking is disabled. GUI FAIL; audio NOT TESTED.

Calling bundled PortMidi Pm_Initialize/Pm_CountDevices/Pm_Terminate separately with
the app-local ALSA config returns successfully (zero devices) despite the same
Unknown SEQ default warning. This does not establish normal confined MIDI support
and does not identify the application crash. Do not infer that warning causes it.

Diagnostic build adds best-effort fatal-signal backtrace logging on Ubuntu Touch
and saves an address-sorted symbol map for the exact unstripped CI executable.
No system debugger, global core settings, AppArmor or audio settings are changed.
Next: build, install verified artifact, reproduce once, resolve module offsets,
fix the confirmed crash location and remove temporary diagnostics when appropriate.
