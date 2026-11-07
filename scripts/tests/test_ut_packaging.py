import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load('runtime', 'stage-ut-runtime.py')
audit = load('audit', 'verify-ut-click.py')


class RuntimeValidation(unittest.TestCase):
    def test_wrong_machine_and_truncated_elf_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'binary'
            for header in (b'\x7fELF', b'\x7fELF\x02\x01' + bytes(12) + b'\x3e\x00'):
                path.write_bytes(header)
                with self.assertRaisesRegex(RuntimeError, 'AArch64'):
                    runtime.aarch64(path)

    def test_missing_dependency_is_fatal(self):
        with patch.object(runtime.subprocess, 'check_output', return_value='libaudio.so.1 => not found\n'):
            with self.assertRaisesRegex(RuntimeError, 'Unresolved dependency'):
                runtime.dependencies(Path('/test/engine'))

    def test_qt6_cannot_leak_into_qt5_package(self):
        with patch.object(runtime.subprocess, 'check_output', return_value='libQt6Core.so.6 => /lib/libQt6Core.so.6 (0x0)\n'):
            with self.assertRaisesRegex(RuntimeError, 'Qt6 dependency'):
                runtime.dependencies(Path('/test/engine'))

    def test_desktop_gl_qt_symbols_are_rejected(self):
        for symbol in ('_ZTI20QOpenGLFunctions_2_1',
                       '_ZN20QOpenGLFunctions_2_125initializeOpenGLFunctionsEv'):
            with patch.object(runtime.subprocess, 'check_output', return_value=symbol):
                with self.assertRaisesRegex(RuntimeError, 'Desktop OpenGL'):
                    runtime.check_gles_symbols(Path('/test/engine'))
        with patch.object(runtime.subprocess, 'check_output', return_value='QOpenGLFunctions'):
            runtime.check_gles_symbols(Path('/test/engine'))

    def test_framework_filter_keeps_media_dependencies_bundled(self):
        for name in ['libQt5Core.so.5', 'libc.so.6', 'libstdc++.so.6', 'libEGL.so.1']:
            self.assertTrue(runtime.FRAMEWORK.match(name), name)
        for name in ['libportaudio.so.2', 'libasound.so.2', 'libpulse.so.0', 'libchromaprint.so.1', 'libcrypto.so.3']:
            self.assertFalse(runtime.FRAMEWORK.match(name), name)


class ClickContentsValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.stage = self.root / 'stage'
        self.build = self.root / 'build'
        self.reports = self.root / 'reports'
        for p in (self.stage, self.build, self.reports):
            p.mkdir()
        (self.reports / 'commit.txt').write_text('abc123\n')
        manifest = {'name': 'bitedj.phsshift', 'version': '0.1.0-test.1', 'architecture': 'arm64',
                    'framework': 'ubuntu-touch-24.04-2.x',
                    'hooks': {'bitedj': {'desktop': 'bitedj.desktop', 'apparmor': 'bitedj.apparmor'}}}
        (self.stage / 'DEBIAN').mkdir()
        (self.stage / 'DEBIAN/manifest').write_text(json.dumps(manifest))
        policy = {'policy_groups': ['audio', 'keep-display-on'], 'policy_version': 2404.2}
        (self.stage / 'bitedj.apparmor').write_text(json.dumps(policy))
        for name in ['bitedj.desktop', 'launch.sh', 'alsa.conf', 'fonts.conf', 'bitedj.png', 'LICENSE',
                     'usr/share/mixxx/skins/BiteDJ/skin.xml', 'usr/share/doc/coreutils/copyright']:
            path = self.stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('test fixture\n')
        # Real ELF fixture; used only for package validation, never installed.
        for name in ['usr/bin/mixxx', 'usr/bin/mkdir', 'lib/aarch64-linux-gnu/alsa-lib/libasound_module_pcm_pulse.so',
                     'lib/aarch64-linux-gnu/alsa-lib/libasound_module_ctl_pulse.so']:
            path = self.stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sys.executable, path)
        (self.stage / 'build-provenance.json').write_text(json.dumps({'commit': 'abc123'}))
        control = self.stage / 'DEBIAN/control'
        control.parent.mkdir(exist_ok=True)
        control.write_text('Package: test-fixture\nVersion: 1\nArchitecture: arm64\nMaintainer: Test <test@example.invalid>\nDescription: temporary validation fixture\n')

    def package(self):
        subprocess.run(['dpkg-deb', '-Znone', '--build', str(self.stage), str(self.build / 'test.click')],
                       check=True, stdout=subprocess.DEVNULL)

    def verify(self):
        with contextlib.redirect_stdout(io.StringIO()):
            audit.verify(self.build, self.reports)

    def test_complete_package_has_checksum(self):
        self.package()
        self.verify()
        report = json.loads((self.reports / 'click-audit.json').read_text())
        self.assertEqual(report['contents_audit'], 'passed')
        self.assertEqual(len(report['sha256']), 64)

    def test_missing_audio_bridge_is_rejected(self):
        (self.stage / 'lib/aarch64-linux-gnu/alsa-lib/libasound_module_pcm_pulse.so').unlink()
        self.package()
        with self.assertRaisesRegex(RuntimeError, 'Missing package file'):
            self.verify()

    def test_reserved_music_permission_is_rejected(self):
        policy = {'policy_groups': ['audio', 'music_files_read', 'keep-display-on'],
                  'policy_version': 2404.2}
        (self.stage / 'bitedj.apparmor').write_text(json.dumps(policy))
        self.package()
        with self.assertRaisesRegex(RuntimeError, 'Unexpected package permissions'):
            self.verify()

    def test_wrong_commit_is_rejected(self):
        (self.stage / 'build-provenance.json').write_text(json.dumps({'commit': 'wrong'}))
        self.package()
        with self.assertRaisesRegex(RuntimeError, 'commit mismatch'):
            self.verify()

    def test_bundled_framework_qt_is_rejected(self):
        (self.stage / 'lib/libQt5Core.so.5').write_text('unexpected')
        self.package()
        with self.assertRaisesRegex(RuntimeError, 'framework Qt'):
            self.verify()


class LauncherContract(unittest.TestCase):
    def test_launcher_uses_app_local_audio_and_preserves_session(self):
        import os
        with tempfile.TemporaryDirectory(prefix='bitedj launch ') as temporary:
            root = Path(temporary)
            app = root / 'app with spaces'
            (app / 'usr/bin').mkdir(parents=True)
            shutil.copy2(SCRIPTS.parent / 'packaging/ubuntu-touch/launch.sh', app / 'launch.sh')
            shutil.copy2(shutil.which('mkdir'), app / 'usr/bin/mkdir')
            engine = app / 'usr/bin/mixxx'
            engine.write_text('#!/bin/sh\nprintf "%s\\n" "$ALSA_CONFIG_PATH" "$ALSA_PLUGIN_DIR" "$PULSE_SERVER" "$QT_QPA_PLATFORM" "$QT_IM_MODULE" "$@"\n')
            engine.chmod(0o755)
            home = root / 'home'
            home.mkdir()
            (home / '.asoundrc').write_text('unchanged system audio\n')
            env = {**os.environ, 'HOME': str(home), 'XDG_CONFIG_HOME': str(home / 'config'),
                   'XDG_DATA_HOME': str(home / 'data'), 'PULSE_SERVER': 'unix:/session/pulse/native'}
            subprocess.run(['sh', str(app / 'launch.sh'), '/music/track with spaces.wav'],
                           env=env, check=True, cwd=root)
            log = (home / 'data/bitedj.phsshift/launch.log').read_text().splitlines()
            self.assertEqual(log[:5], [str(app / 'alsa.conf'), str(app / 'lib/aarch64-linux-gnu/alsa-lib'),
                                      'unix:/session/pulse/native', 'ubuntumirclient', 'maliit'])
            self.assertIn('--full-screen', log)
            self.assertIn('/music/track with spaces.wav', log)
            self.assertEqual((home / '.asoundrc').read_text(), 'unchanged system audio\n')


if __name__ == '__main__':
    unittest.main()
