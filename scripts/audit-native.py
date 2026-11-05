#!/usr/bin/env python3
"""Fail closed on missing executable, wrong ELF machine, unresolved libraries or skin."""
import json
import pathlib
import struct
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
binaries = list(root.glob("usr/bin/mixxx"))
if len(binaries) != 1:
    raise SystemExit("Expected exactly one installed usr/bin/mixxx")
binary = binaries[0]
header = binary.read_bytes()[:20]
if header[:6] != b"\x7fELF\x02\x01" or struct.unpack("<H", header[18:20])[0] != 183:
    raise SystemExit("Executable is not little-endian ELF64 AArch64")
result = subprocess.run(["ldd", str(binary)], capture_output=True, text=True)
if result.returncode or "not found" in result.stdout:
    raise SystemExit(result.stdout + result.stderr)
skins = list(root.glob("usr/share/**/skins/**/skin.xml"))
if not skins:
    raise SystemExit("No installed skin.xml")
print(json.dumps({"elf": "PASS", "runner_dependencies": "PASS",
                  "skins": [str(p) for p in skins],
                  "target_runtime": "NOT TESTED", "hardware": "NOT TESTED",
                  "ldd": result.stdout}, indent=2))
