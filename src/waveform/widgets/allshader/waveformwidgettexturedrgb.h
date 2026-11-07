#pragma once

#include <QtGui/qopengl.h>

// This optional renderer uses desktop display lists and immediate-mode GL.
#if !defined(QT_OPENGL_ES_2)

#include "util/class.h"
#include "waveform/renderers/allshader/waveformrenderertextured.h"
#include "waveform/widgets/allshader/waveformwidget.h"

class WaveformWidgetFactory;

namespace allshader {
class WaveformWidgetTexturedRGB;
}

class allshader::WaveformWidgetTexturedRGB final : public allshader::WaveformWidget {
    Q_OBJECT
  public:
    WaveformWidgetType::Type getType() const override {
        return WaveformWidgetType::AllShaderTexturedRGB;
    }

    static inline QString getWaveformWidgetName() {
        return tr("RGB");
    }
    static constexpr bool useOpenGl() {
        return true;
    }
    static constexpr bool useOpenGles() {
        return false;
    }
    static constexpr bool useOpenGLShaders() {
        return true;
    }
    static constexpr bool useTextureForWaveform() {
        return true;
    }
    static constexpr WaveformWidgetCategory category() {
        return WaveformWidgetCategory::AllShader;
    }

  protected:
    void castToQWidget() override;
    void paintEvent(QPaintEvent* event) override;

  private:
    WaveformWidgetTexturedRGB(const QString& group, QWidget* parent);
    friend class ::WaveformWidgetFactory;

    DISALLOW_COPY_AND_ASSIGN(WaveformWidgetTexturedRGB);
};

#endif // !QT_OPENGL_ES_2
