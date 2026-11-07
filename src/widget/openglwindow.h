#pragma once

#ifdef BITEDJ_UBUNTU_TOUCH
#include <QOpenGLWidget>
#else
#include <QOpenGLWindow>
#endif

class WGLWidget;
class TrackDropTarget;

/// Helper class used by wglwidgetqopengl

#ifdef BITEDJ_UBUNTU_TOUCH
class OpenGLWindow : public QOpenGLWidget {
#else
class OpenGLWindow : public QOpenGLWindow {
#endif
    Q_OBJECT

  public:
    OpenGLWindow(WGLWidget* pWidget);
    ~OpenGLWindow();

    void widgetDestroyed();
#ifdef BITEDJ_UBUNTU_TOUCH
    bool isExposed() const { return isVisible(); }
#endif

  private:
    void initializeGL() override;
    void paintGL() override;
    void resizeGL(int w, int h) override;
    bool event(QEvent* pEv) override;

    WGLWidget* m_pWidget;
    TrackDropTarget* m_pTrackDropTarget;
};
