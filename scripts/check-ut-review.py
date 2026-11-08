#!/usr/bin/env python3
"""Permit only the intentional music-player reserved permission review finding."""
import re
import sys
from pathlib import Path

text = re.sub(r"\x1b\[[0-9;]*m", "", Path(sys.argv[1]).read_text())
if "Running review on " not in text:
    raise SystemExit("Missing Click review output")
review = text.rsplit("Running review on ", 1)[1]
if "\nErrors\n------\n" in review:
    errors = review.split("\nErrors\n------\n", 1)[1]
    errors = errors.split("\nWarnings\n", 1)[0]
    findings = re.findall(r"^ - ([^\n]+)$", errors, re.M)
    allowed = "security:policy_groups_safe:bitedj:music_files_read"
    if not findings or any(item != allowed for item in findings):
        raise SystemExit("Unexpected Click review errors: " + repr(findings))
    print("PASS: only intentional music_files_read reserved-policy finding")
elif not re.search(r": (?:OK|PASS|pass)\s*$", review, re.M):
    raise SystemExit("Unrecognized Click review result")
else:
    print("PASS: Click review has no errors")
