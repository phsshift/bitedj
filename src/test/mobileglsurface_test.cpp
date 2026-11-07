#include <gtest/gtest.h>

#include <QOpenGLWidget>
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
