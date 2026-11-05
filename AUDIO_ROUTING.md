# Audio routing research
Upstream AudioDeviceSettings exposes Master, Booth, Headphones; buildOptions enumerates
nonoverlapping adjacent stereo pairs up to each reported device output count.
Settings are staged until Apply and changes are guarded while decks play.
SoundManagerConfig persists paths; reconnect logic relinks device identifiers.
Do not replace the existing engine or write ALSA system configuration.

Still required: inspect AudioPathType deck index semantics and external mixer controls;
extend touch panel to Deck A/B and explicit Internal/External mode, enforce no main sum
in External; expose backend/rate/buffer selection; per-device profile management;
supported format/rate/layout validation and output test generator.
The current code is not claimed to implement these missing functions.

MOTU Internal target: Main 1/2 + Headphones 3/4, then reverse.
MOTU External target: Deck A 1/2 + Deck B 3/4, then reverse.
Pioneer External 8ch is a future template; apply only to actual detected >=8ch hardware.
Keep physical channels, logical buses, decks and mixer mode separate.
No physical output or eight-channel software test performed.
