# Test.24 confirmed startup crash

Target run 42401722167 compile/unit tests/review/audit PASS; native visual tests FAIL.
Installed verified test.24. Normal shortcut still fails before main UI.
Captured stack: pthread_mutex_lock -> libusb_get_device_list ->
BulkEnumerator::queryDevices+0xdc -> ControllerManager::updateControllerList+0xfc
-> ControllerManager::slotSetUpDevices+0xcc. App offsets resolved against exact
CI engine-symbols.txt. This localizes the crash to USB Bulk enumeration.

BulkEnumerator ignored libusb_init's return value, then used a null context
when initialization failed. libusb interprets null as its default context,
which does not exist after failed init. Add explicit initialization failure
handling, skip discovery without a context, guard teardown, handle negative
device-list results and skip unreadable descriptors before inspecting them.
USB bulk discovery remains functional where initialization succeeds. No new
AppArmor/device permission or system configuration changes are introduced.

No GUI/audio success claimed. Next: run CI and deterministic USB-error regression
checks, install verified replacement, retry normal shortcut and inspect logs.
