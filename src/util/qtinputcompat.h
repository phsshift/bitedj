#pragma once

#include <QMouseEvent>
#include <QTouchEvent>
#include <QWidget>
#include <optional>
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
#include <QPointingDevice>
#endif

namespace mixxx::qt {
inline QPointF mouseGlobalPosition(const QMouseEvent* event) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return event->globalPosition();
#else
    return event->screenPos();
#endif
}

inline QPointF mousePosition(const QMouseEvent* event) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return event->position();
#else
    return event->localPos();
#endif
}

inline QPointF mouseScenePosition(const QMouseEvent* event) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return event->scenePosition();
#else
    return event->windowPos();
#endif
}

inline QPointF mapToGlobal(const QWidget* widget, QPointF position) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return widget->mapToGlobal(position);
#else
    return widget->mapToGlobal(position.toPoint());
#endif
}

inline std::optional<QPointF> inputGlobalPosition(const QEvent* event) {
    if (event->type() == QEvent::MouseButtonPress) {
        return mouseGlobalPosition(static_cast<const QMouseEvent*>(event));
    }
    const auto* touch = static_cast<const QTouchEvent*>(event);
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    if (!touch->points().isEmpty()) {
        return touch->points().first().globalPosition();
    }
#else
    if (!touch->touchPoints().isEmpty()) {
        return touch->touchPoints().first().screenPos();
    }
#endif
    return std::nullopt;
}

inline QPointF mapFromGlobal(const QWidget* widget, QPointF position) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return widget->mapFromGlobal(position);
#else
    return widget->mapFromGlobal(position.toPoint());
#endif
}

inline auto mouseDevice(const QMouseEvent* event = nullptr) {
#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
    return event && event->pointingDevice() ? event->pointingDevice()
                                          : QPointingDevice::primaryPointingDevice();
#else
    return event ? event->source() : Qt::MouseEventSynthesizedByApplication;
#endif
}
using MouseDevice = decltype(mouseDevice());
} // namespace mixxx::qt
