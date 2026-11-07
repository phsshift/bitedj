#!/usr/bin/env python3
"""Compare existing goldens with explicit fonts on a disposable CI runner."""
import json
import os
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape

if (os.environ.get('GITHUB_ACTIONS') != 'true' or
        os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted' or
        not os.environ.get('RUNNER_TEMP')):
    raise SystemExit('Refusing visual font probes outside GitHub-hosted CI')

root = Path.cwd()
out = root / 'reports' / 'visual-font-probes'
out.mkdir(parents=True, exist_ok=True)
results = []
for family in ('DejaVu Sans', 'Liberation Sans', 'Noto Sans'):
    tag = family.lower().replace(' ', '-')
    config = Path(os.environ['RUNNER_TEMP']) / f'bitedj-font-probe-{tag}.conf'
    config.write_text('''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <include ignore_missing="no">/etc/fonts/fonts.conf</include>
  <match target="pattern">
    <test name="family" compare="eq"><string>Inter</string></test>
    <edit name="family" mode="assign" binding="strong"><string>''' + escape(family) + '''</string></edit>
  </match>
  <match target="font">
    <edit name="rgba" mode="assign"><const>none</const></edit>
  </match>
</fontconfig>
''')
    env = dict(os.environ, FONTCONFIG_FILE=str(config))
    match = subprocess.check_output(
        ['fc-match', '-f', '%{family}\n', 'Inter'], env=env, text=True).strip()
    if family not in (name.strip() for name in match.split(',')):
        results.append({'requested': family, 'resolved': match,
                        'exit_code': 'font-unavailable'})
        (out / 'results.json').write_text(json.dumps(results, indent=2) + '\\n')
        print(json.dumps(results[-1]), flush=True)
        continue
    with (out / f'{tag}.log').open('w') as log:
        try:
            result = subprocess.run(
                ['build/bitedj-visual-test', '--out', str(out / tag),
                 'src/test/visual/beat_grid_lines.json'],
                env=env, stdout=log, stderr=subprocess.STDOUT, timeout=120)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 'timeout'
    results.append({'requested': family, 'resolved': match, 'exit_code': code})
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results[-1]), flush=True)
# Diagnostic comparisons never replace or suppress the required visual tests.
