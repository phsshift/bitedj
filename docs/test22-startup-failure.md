# Test.22 startup failure

Installed 0.1.0-test.22, commit 00b2779ab51365a30ce69a8bfeb4a562f079489d.
Phone library relocations PASS; previous Qt OpenGL symbol mismatch resolved.
Normal shortcut attempts reach Qt/Lomiri session creation, then SIGTRAP.
Fatal log: GLib cannot create the gdbus thread: Resource temporarily unavailable.
Earlier in both attempts, process-wide mlockall succeeds. Application code uses
MCL_CURRENT | MCL_FUTURE | MCL_ONFAULT before Qt initialization. Session default
memlock is 491053056 bytes. This makes memlock exhaustion a plausible cause of
new thread stack allocation failure; it is not yet confirmed by syscall tracing
or by a successful build with memory locking disabled. Available memory at
inspection was about 2 GB; process count limit was 12878, system threads about
1481. Those observations do not establish the exact failed allocation.

A separate preceding message says Cannot find EGLConfig and context creation
fails with 0x3001 (EGL_NOT_INITIALIZED). Whether this is also caused by memory
allocation constraints or an independent graphics issue is not yet established.

Prepared fix: on BITEDJ_UBUNTU_TOUCH only, leave process memory pageable instead
of locking all present/future allocations. Preserve desktop memory-lock behavior,
full audio engine and system limits. Do not raise global limits or alter drivers.
Performance/latency and successful phone launch remain NOT TESTED.

Reference: https://man7.org/linux/man-pages/man2/mlock.2.html (MCL_FUTURE can make
later mappings/heap/stack growth fail at the locked-memory limit).

User initially requested investigation then pause until usage renews, then sent
continue before the checkpoint was saved. Continue revokes the pending pause.
No background CI monitor was running. No global system/audio/VPN changes made.
Next: compile this target-specific change on GitHub, install verified artifact,
retry normal shortcut, then diagnose EGL separately if still failing.
