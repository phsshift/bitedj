#!/usr/bin/env python3
"""Stage the real SDK-built engine and its non-framework runtime into a Click."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

# Keep Qt, the dynamic loader, C/C++ runtime and graphics drivers on the
# framework ABI. Never ship a runner's Qt platform or GPU integration plugins.
FRAMEWORK = re.compile(
    r'^(?:libQt5|ld-linux-aarch64|lib(?:c|m|dl|rt|pthread|resolv|util|anl)\.so|'
    r'libstdc\+\+\.so|libgcc_s\.so|lib(?:GL|GLX|GLdispatch|EGL|GLESv[12])\.so)')


def aarch64(path):
    with path.open("rb") as stream:
        header = stream.read(20)
    if len(header) < 20 or header[:5] != b'\x7fELF\x02' or header[5] != 1 or int.from_bytes(header[18:20], 'little') != 183:
        raise RuntimeError(f'Expected little-endian AArch64 ELF: {path}')


def dependencies(path):
    output = subprocess.check_output(['ldd', str(path)], text=True, stderr=subprocess.STDOUT)
    result = []
    for line in output.splitlines():
        if 'not found' in line:
            raise RuntimeError(f'Unresolved dependency of {path}: {line}')
        match = re.match(r'\s*(\S+) => (/\S+) ', line)
        if match:
            name, resolved = match.groups()
            if name.startswith('libQt6'):
                raise RuntimeError('Qt6 dependency in Qt5 target build')
            result.append((name, Path(resolved)))
    return result


def stage(source, install, reports):
    binary = install / 'usr/bin/mixxx'
    aarch64(binary)
    if not (install / 'usr/share/mixxx/skins/BiteDJ/skin.xml').is_file():
        raise RuntimeError('BiteDJ skin is missing')
    libdir = install / 'lib/aarch64-linux-gnu'
    libdir.mkdir(parents=True, exist_ok=True)
    plugins = Path('/usr/lib/aarch64-linux-gnu/alsa-lib')
    bridge = plugins / 'libasound_module_pcm_pulse.so'
    if not bridge.is_file():
        raise RuntimeError('ALSA PulseAudio plugin missing from SDK')
    todo = [binary]
    for name in ('libasound_module_pcm_pulse.so', 'libasound_module_ctl_pulse.so'):
        src = plugins / name
        aarch64(src)
        target = libdir / 'alsa-lib' / name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(src, target)
        todo.append(src)
    bundled = {}
    framework = {}
    checked = set()
    while todo:
        path = todo.pop()
        if path.resolve() in checked:
            continue
        checked.add(path.resolve())
        for name, resolved in dependencies(path):
            if FRAMEWORK.match(name):
                framework[name] = str(resolved)
                continue
            aarch64(resolved)
            digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
            if name in bundled:
                if bundled[name]['sha256'] != digest:
                    raise RuntimeError(f'Conflicting libraries named {name}')
                continue
            shutil.copy2(resolved, libdir / name)
            bundled[name] = {'source': str(resolved), 'sha256': digest}
            todo.append(resolved)
    packaging = source / 'packaging/ubuntu-touch'
    for name in ('launch.sh', 'alsa.conf', 'bitedj.desktop', 'bitedj.apparmor', 'fonts.conf'):
        shutil.copy2(packaging / name, install / name)
    shutil.copy2(source / 'res/skins/BiteDJ/images/bitedj_logo.png', install / 'bitedj.png')
    fontdir = install / 'fonts'
    fontdir.mkdir(exist_ok=True)
    inter = list(Path('/usr/share/fonts').rglob('Inter*.otf')) + list(Path('/usr/share/fonts').rglob('Inter*.ttf'))
    if not inter:
        raise RuntimeError('Inter fonts missing from SDK')
    for font in inter:
        shutil.copy2(font, fontdir / font.name)
    copyright_path = Path('/usr/share/doc/fonts-inter/copyright')
    shutil.copy2(copyright_path, fontdir / 'Inter-copyright')
    shutil.copy2(source / 'LICENSE', install / 'LICENSE')
    build_number = (reports / 'build-number.txt').read_text().strip()
    if not build_number.isdigit():
        raise RuntimeError('Invalid CI build number')
    manifest = {
        'name': 'bitedj.phsshift', 'version': f'0.1.0-test.{build_number}',
        'title': 'BiteDJ', 'description': 'BiteDJ two-deck DJ mixer for Ubuntu Touch (test build)',
        'maintainer': 'phsshift', 'architecture': 'arm64',
        'framework': 'ubuntu-touch-24.04-2.x',
        'hooks': {'bitedj': {'desktop': 'bitedj.desktop', 'apparmor': 'bitedj.apparmor'}}
    }
    (install / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    commit = (reports / 'commit.txt').read_text().strip()
    provenance = {'commit': commit, 'version': manifest['version'], 'platform': 'ubuntu-touch',
                  'qt': 'Qt5 from pinned Clickable SDK', 'unit_tests': 'passed',
                  'native_visual_tests': 'separate CI job; do not infer success',
                  'target_gui': 'NOT TESTED', 'system_audio': 'NOT TESTED', 'MOTU': 'DEFERRED'}
    (install / 'build-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    (reports / 'runtime-bundle.json').write_text(json.dumps({'bundled': bundled, 'framework': framework, **provenance}, indent=2) + '\n')
    # Stripping only the packaged copy preserves diagnostic symbols in build/.
    subprocess.run(['strip', '--strip-unneeded', str(binary)], check=True)
    for path in libdir.rglob('*.so*'):
        subprocess.run(['strip', '--strip-unneeded', str(path)], check=True)
    print(json.dumps({'staged': str(install), 'bundled_libraries': len(bundled), **provenance}))


if __name__ == '__main__':
    stage(*(Path(arg).resolve() for arg in sys.argv[1:]))
