#include "controllers/bulk/bulkenumerator.h"

#include <libusb.h>

#include "controllers/bulk/bulkcontroller.h"
#include "controllers/bulk/bulksupported.h"
#include "moc_bulkenumerator.cpp"

BulkEnumerator::BulkEnumerator(UserSettingsPointer pConfig)
        : ControllerEnumerator(),
          m_context(nullptr),
          m_pConfig(pConfig) {
    const int error = libusb_init(&m_context);
    if (error != LIBUSB_SUCCESS) {
        qWarning() << "USB Bulk discovery unavailable:" << libusb_error_name(error);
        m_context = nullptr;
    }
}

BulkEnumerator::~BulkEnumerator() {
    qDebug() << "Deleting USB Bulk devices...";
    while (m_devices.size() > 0) {
        delete m_devices.takeLast();
    }
    if (m_context) {
        libusb_exit(m_context);
    }
}

static bool is_interesting(struct libusb_device_descriptor *desc) {
    for (int i = 0; bulk_supported[i].vendor_id; ++i) {
        if ((bulk_supported[i].vendor_id == desc->idVendor) &&
            (bulk_supported[i].product_id == desc->idProduct)) {
            return true;
        }
    }
    return false;
}

QList<Controller*> BulkEnumerator::queryDevices() {
    qDebug() << "Scanning USB Bulk devices:";
    // A failed init leaves no context. Passing nullptr would ask libusb for
    // its default context, which does not exist after initialization failed.
    if (!m_context) {
        return m_devices;
    }
    libusb_device** list = nullptr;
    const ssize_t cnt = libusb_get_device_list(m_context, &list);
    if (cnt < 0) {
        qWarning() << "Cannot enumerate USB Bulk devices:"
                   << libusb_error_name(static_cast<int>(cnt));
        return m_devices;
    }
    ssize_t i = 0;
    int err = 0;

    for (i = 0; i < cnt; i++) {
        libusb_device *device = list[i];
        struct libusb_device_descriptor desc;

        const int descriptorError = libusb_get_device_descriptor(device, &desc);
        if (descriptorError != LIBUSB_SUCCESS) {
            qWarning() << "Cannot read USB Bulk device descriptor:"
                       << libusb_error_name(descriptorError);
            continue;
        }
        if (is_interesting(&desc)) {
            struct libusb_device_handle* handle = nullptr;
            err = libusb_open(device, &handle);
            if (err) {
                qWarning() << "Error opening a device:" << libusb_error_name(err);
                continue;
            }

            BulkController* currentDevice =
                    new BulkController(m_context, handle, &desc);
            m_devices.push_back(currentDevice);
        }
    }
    libusb_free_device_list(list, 1);
    return m_devices;
}
