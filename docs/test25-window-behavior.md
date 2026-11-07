# Test.25 interface and window findings

User confirmed main interface launches. Saved screenshot
screenshot20261107_221953254.png shows a functioning BiteDJ settings page in a
minimum-size 480x420 logical window at the upper left of a landscape screen.
GUI launch PASS; fullscreen FAIL; track loading and audible playback NOT TESTED.
App registers a stereo float32 44100 Hz stream with PulseAudio. This proves
output-device initialization, not audible sound. Later user reports multiple
windows opening without a command. A single BiteDJ process was observed; it
subsequently stopped. Do not infer multiple processes from extra windows.

Application GL controls embed separate QOpenGLWindows via createWindowContainer.
This creates native child surfaces and is a plausible cause of separately
managed windows on Mir. Mobile replacement uses QOpenGLWidget children rendered
into FBOs and composed in the main window, preserving existing waveform/meter
renderers and the desktop QOpenGLWindow path. Add a structural Qt unit test that
the render surface is a child widget, not another top-level window. Real Mir
rendering and frame-rate behavior still require the replacement phone test.

Enable --full-screen in mobile launcher; use APP_ID for desktop-file association.
Local StartInFullscreen preference was backed up, enabled and app restarted;
user then reported many windows, so automatic relaunches stopped pending repair.
No shell desktop-mode, audio, graphics driver or security changes.

Qt reference: https://doc.qt.io/archives/qt-5.15/qopenglwidget.html
(QOpenGLWidget renders into its own FBO; makeCurrent binds it; no native window.)
