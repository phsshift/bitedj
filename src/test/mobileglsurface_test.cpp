#include <gtest/gtest.h>

#include <QOpenGLWidget>
#include <QApplication>
#include <QWidget>

#include "test/mixxxtest.h"
#include "waveform/waveformwidgetfactory.h"
#include "widget/openglwindow.h"
#include "widget/wglwidget.h"

class MobileGLSurfaceTest : public MixxxTest {};

TEST_F(MobileGLSurfaceTest, RenderSurfaceIsAChildWidgetNotAnotherWindow) {
    WaveformWidgetFactory::getSurfaceFormat(config());
    QWidget mainWindow;
    WGLWidget waveform(&mainWindow);
    OpenGLWindow surface(&waveform);
    EXPECT_EQ(surface.parentWidget(), &waveform);
    EXPECT_FALSE(surface.isWindow());
    EXPECT_EQ(surface.window(), &mainWindow);
    EXPECT_TRUE(waveform.findChildren<QOpenGLWidget*>().contains(&surface));
}

namespace {
class OwnerEventProbe : public WGLWidget {
  public:
    explicit OwnerEventProbe(QWidget* parent) : WGLWidget(parent) {}
    int privateEvents = 0;

  protected:
    bool event(QEvent* event) override {
        if (event->type() == QEvent::User) {
            ++privateEvents;
            return true;
        }
        return WGLWidget::event(event);
    }
};
} // namespace

TEST_F(MobileGLSurfaceTest, SurfacePrivateEventsDoNotReenterOwner) {
    WaveformWidgetFactory::getSurfaceFormat(config());
    QWidget mainWindow;
    OwnerEventProbe waveform(&mainWindow);
    OpenGLWindow surface(&waveform);
    QEvent privateEvent(QEvent::User);
    QApplication::sendEvent(&surface, &privateEvent);
    EXPECT_EQ(waveform.privateEvents, 0);
}
