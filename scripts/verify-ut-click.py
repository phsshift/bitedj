#!/usr/bin/env python3
"""Audit the packaged Click, rather than just its pre-packaging directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import importlib.util
spec = importlib.util.spec_from_file_location('stage_ut', Path(__file__).with_name('stage-ut-runtime.py'))
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def verify(build, reports):
    packages = list(build.rglob('*.click'))
    if len(packages) != 1:
        raise RuntimeError(f'Expected exactly one Click, found {len(packages)}')
    package = packages[0]
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        subprocess.run(['dpkg-deb', '--extract', str(package), str(root)], check=True)
        # Click stores its manifest in the control archive, outside the payload.
        control = root / 'DEBIAN'
        subprocess.run(['dpkg-deb', '--control', str(package), str(control)], check=True)
        manifest = json.loads((control / 'manifest').read_text())
        if manifest['architecture'] != 'arm64' or manifest['framework'] != 'ubuntu-touch-24.04-2.x':
            raise RuntimeError('Incorrect package target')
        hooks = manifest['hooks']['bitedj']
        policy = json.loads((root / hooks['apparmor']).read_text())
        if policy != {'policy_groups': ['audio', 'keep-display-on', 'music_files_read'], 'policy_version': 2404.2}:
            raise RuntimeError('Unexpected package permissions')
        required = [hooks['desktop'], 'launch.sh', 'alsa.conf', 'fonts.conf', 'bitedj.png',
                    'LICENSE', 'build-provenance.json', 'usr/bin/mixxx', 'usr/bin/mkdir',
                    'usr/share/doc/coreutils/copyright',
                    'usr/share/mixxx/skins/BiteDJ/skin.xml',
                    'lib/aarch64-linux-gnu/alsa-lib/libasound_module_pcm_pulse.so',
                    'lib/aarch64-linux-gnu/alsa-lib/libasound_module_ctl_pulse.so']
        for name in required:
            if not (root / name).is_file() or not (root / name).stat().st_size:
                raise RuntimeError(f'Missing package file: {name}')
        runtime.aarch64(root / 'usr/bin/mixxx')
        runtime.aarch64(root / 'usr/bin/mkdir')
        if list(root.rglob('libQt*.so*')) or list(root.rglob('libqpa-*.so')):
            raise RuntimeError('Package must use framework Qt and platform integration')
        for library in (root / 'lib').rglob('*.so*'):
            runtime.aarch64(library)
        provenance = json.loads((root / 'build-provenance.json').read_text())
        if provenance['commit'] != (reports / 'commit.txt').read_text().strip():
            raise RuntimeError('Package source commit mismatch')
        summary = {'package': str(package), 'sha256': hashlib.sha256(package.read_bytes()).hexdigest(),
                   'manifest': manifest, 'provenance': provenance, 'contents_audit': 'passed'}
        (reports / 'click-audit.json').write_text(json.dumps(summary, indent=2) + '\n')
        (reports / 'SHA256SUMS').write_text(f"{summary['sha256']}  {package.name}\n")
        print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    verify(*(Path(arg).resolve() for arg in sys.argv[1:]))
