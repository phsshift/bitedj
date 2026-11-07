#include <gtest/gtest.h>
#include <libusb.h>

#include "controllers/bulk/bulkenumerator.h"

namespace {
enum class UsbMode { Real, InitFailure, ListFailure, EmptyList };
thread_local UsbMode s_mode = UsbMode::Real;
thread_local int s_listCalls = 0;
thread_local int s_exitCalls = 0;
thread_local int s_freeCalls = 0;

struct FakeUsbScope {
    explicit FakeUsbScope(UsbMode mode) {
        s_mode = mode;
        s_listCalls = s_exitCalls = s_freeCalls = 0;
    }
    ~FakeUsbScope() { s_mode = UsbMode::Real; }
};
} // namespace

extern "C" {
int __real_libusb_init(libusb_context** context);
ssize_t __real_libusb_get_device_list(libusb_context* context, libusb_device*** list);
void __real_libusb_exit(libusb_context* context);
void __real_libusb_free_device_list(libusb_device** list, int unrefDevices);

int __wrap_libusb_init(libusb_context** context) {
    if (s_mode == UsbMode::Real) {
        return __real_libusb_init(context);
    }
    *context = s_mode == UsbMode::InitFailure ? nullptr
                                            : reinterpret_cast<libusb_context*>(1);
    return s_mode == UsbMode::InitFailure ? LIBUSB_ERROR_ACCESS : LIBUSB_SUCCESS;
}
ssize_t __wrap_libusb_get_device_list(libusb_context* context, libusb_device*** list) {
    if (s_mode == UsbMode::Real) {
        return __real_libusb_get_device_list(context, list);
    }
    ++s_listCalls;
    *list = nullptr;
    return s_mode == UsbMode::ListFailure ? LIBUSB_ERROR_IO : 0;
}
void __wrap_libusb_exit(libusb_context* context) {
    if (s_mode == UsbMode::Real) {
        __real_libusb_exit(context);
    } else {
        ++s_exitCalls;
    }
}
void __wrap_libusb_free_device_list(libusb_device** list, int unrefDevices) {
    if (s_mode == UsbMode::Real) {
        __real_libusb_free_device_list(list, unrefDevices);
    } else {
        ++s_freeCalls;
    }
}
} // extern "C"

TEST(BulkEnumeratorFailureTest, InitializationFailureSkipsDiscoveryAndTeardown) {
    FakeUsbScope fake(UsbMode::InitFailure);
    {
        BulkEnumerator enumerator(UserSettingsPointer{});
        EXPECT_TRUE(enumerator.queryDevices().isEmpty());
        EXPECT_TRUE(enumerator.queryDevices().isEmpty());
    }
    EXPECT_EQ(s_listCalls, 0);
    EXPECT_EQ(s_exitCalls, 0);
    EXPECT_EQ(s_freeCalls, 0);
}

TEST(BulkEnumeratorFailureTest, ListFailureDoesNotFreeAnInvalidList) {
    FakeUsbScope fake(UsbMode::ListFailure);
    {
        BulkEnumerator enumerator(UserSettingsPointer{});
        EXPECT_TRUE(enumerator.queryDevices().isEmpty());
    }
    EXPECT_EQ(s_listCalls, 1);
    EXPECT_EQ(s_exitCalls, 1);
    EXPECT_EQ(s_freeCalls, 0);
}

TEST(BulkEnumeratorFailureTest, SuccessfulInitializationStillScans) {
    FakeUsbScope fake(UsbMode::EmptyList);
    {
        BulkEnumerator enumerator(UserSettingsPointer{});
        EXPECT_TRUE(enumerator.queryDevices().isEmpty());
    }
    EXPECT_EQ(s_listCalls, 1);
    EXPECT_EQ(s_exitCalls, 1);
    EXPECT_EQ(s_freeCalls, 1);
}
