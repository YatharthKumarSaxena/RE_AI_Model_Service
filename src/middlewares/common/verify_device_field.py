from flask import request

from src.responses.common.error_handler import (
    throw_internal_server_error,
    throw_missing_fields_error,
    log_middleware_error,
    throw_bad_request_error,
    throw_validation_error
)

from src.utils.id_validators import (
    is_valid_uuid,
    is_valid_device_name_length
)

from src.utils.enum_helpers import (
    DeviceTypeHelper
)

from src.configs.field_lengths import (
    FIELD_LENGTHS
)

from src.utils.time_stamps import (
    log_with_time
)

from src.configs.headers import (
    DEVICE_HEADERS
)


def verify_device_field():

    try:

        uuid = request.headers.get(
            DEVICE_HEADERS["DEVICE_UUID"]
        )

        name = request.headers.get(
            DEVICE_HEADERS["DEVICE_NAME"]
        )

        device_type = request.headers.get(
            DEVICE_HEADERS["DEVICE_TYPE"]
        )

        device_uuid = None
        device_name = None
        device_type_value = None

        # Device UUID is mandatory
        if (
            not uuid
            or not uuid.strip()
        ):

            log_middleware_error(
                "verifyDeviceField",
                "Missing device UUID in headers"
            )

            return throw_missing_fields_error(
                [
                    "Device UUID (x-device-uuid) "
                    "is required in request headers"
                ]
            )

        uuid = uuid.strip()

        if not is_valid_uuid(uuid):

            log_middleware_error(
                "verifyDeviceField",
                "Invalid Device ID format"
            )

            return throw_validation_error(
                [
                    {
                        "field": "deviceUUID",
                        "message": (
                            "Invalid deviceUUID format. "
                            "Must be a valid UUID v4"
                        ),
                        "received": uuid
                    }
                ]
            )

        device_uuid = uuid

        # Device name is optional
        if (
            name
            and name.strip()
        ):

            name = name.strip()

            if not is_valid_device_name_length(
                name
            ):

                log_middleware_error(
                    "verifyDeviceField",
                    "Invalid Device Name length"
                )

                return throw_validation_error(
                    [
                        {
                            "field": "deviceName",
                            "message": (
                                "Invalid length, must be between "
                                f"{FIELD_LENGTHS['deviceNameLength']['min']} "
                                "and "
                                f"{FIELD_LENGTHS['deviceNameLength']['max']} "
                                "characters"
                            ),
                            "received": name
                        }
                    ]
                )

            device_name = name

        # Device type is optional
        if (
            device_type
            and device_type.strip()
        ):

            device_type_value = (
                device_type.strip()
            )

            if not DeviceTypeHelper[
                "validate"
            ](device_type_value):

                log_middleware_error(
                    "verifyDeviceField",
                    "Invalid Device Type"
                )

                valid_types = ", ".join(
                    DeviceTypeHelper[
                        "get_valid_values"
                    ]()
                )

                return throw_bad_request_error(
                    (
                        "Invalid device type. "
                        f"Must be one of: {valid_types}"
                    )
                )

        request.device = {
            "deviceUUID": device_uuid,
            "deviceName": device_name,
            "deviceType": device_type_value
        }

        log_with_time(
            "✅ Device field verification passed "
            f"for device ID: {device_uuid}"
        )

        return None

    except Exception as error:

        device_uuid = request.headers.get(
            DEVICE_HEADERS["DEVICE_UUID"],
            "Unauthorized Device ID"
        )

        log_with_time(
            "⚠️ Error occurred while validating "
            "the Device field having device id: "
            f"{device_uuid}"
        )

        return throw_internal_server_error(
            error
        )