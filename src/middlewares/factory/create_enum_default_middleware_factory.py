from flask import request

from src.utils.time_stamps import log_with_time


# ============================================================
# ENUM DEFAULT MIDDLEWARE FACTORY
# ============================================================

def create_enum_default_middleware(
    middleware_name,
    enum_helper
):

    def middleware():

        try:

            # =================================================
            # GET MODEL FROM REQUEST
            # =================================================

            request_data = request.get_json(
                silent=True
            ) or {}

            value = request_data.get(
                "model"
            )

            if not value:
                value = request.form.get(
                    "model"
                )

            enum_class = enum_helper[
                "enum_class"
            ]

            default_value = enum_class.DEFAULT.value

            # =================================================
            # VALUE NOT PROVIDED
            # =================================================

            if not value:

                request.entity_model = default_value

                log_with_time(
                    f"⚠️ [{middleware_name}] "
                    f"Model not provided. "
                    f"Using default model: {default_value}"
                )

                return None

            # =================================================
            # INVALID VALUE
            # =================================================

            if not enum_helper["validate"](value):

                request.entity_model = default_value

                log_with_time(
                    f"⚠️ [{middleware_name}] "
                    f"Invalid model '{value}'. "
                    f"Using default model: {default_value}"
                )

                return None

            # =================================================
            # VALID VALUE
            # =================================================

            request.entity_model = value

            log_with_time(
                f"✅ [{middleware_name}] "
                f"Model selected successfully: {value}"
            )

            return None

        except Exception as error:

            log_with_time(
                f"❌ [{middleware_name}] "
                f"Unexpected error: {str(error)}"
            )

            raise

    return middleware