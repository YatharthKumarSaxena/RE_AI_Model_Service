from flask import request

from src.services.classification_service import (
    classify_entity
)

from src.responses.success.classification import (
    entity_type_bulk_import_success
)

from src.responses.common.error_handler import (
    throw_internal_server_error
)

from src.configs.validation_sets import (
    validation_sets
)

from src.configs.required_fields import (
    required_fields
)

from src.utils.time_stamps import log_with_time
from src.utils.log_error import error_message


def import_entity_type_controller():

    try:

        # ========================================================
        # GET PARSED IMPORT DATA
        # ========================================================

        import_data = getattr(
            request,
            "import_data",
            None
        )

        if not import_data:

            raise ValueError(
                "No import data found."
            )

        rows = import_data.get(
            "rows",
            []
        )

        # ========================================================
        # GET SELECTED MODEL
        # ========================================================

        entity_model = getattr(
            request,
            "entity_model",
            None
        )

        if not entity_model:

            raise ValueError(
                "Entity classification model not found."
            )

        # ========================================================
        # VALIDATION SET
        # ========================================================

        validation_set = validation_sets[
            "import_entity_type_validation_set"
        ]

        # ========================================================
        # REQUIRED FIELDS
        # ========================================================

        import_required_fields = required_fields[
            "import_entity_type_field"
        ]

        # ========================================================
        # RESULT COLLECTIONS
        # ========================================================

        processed_rows = []

        valid_rows_count = 0
        invalid_rows_count = 0

        # ========================================================
        # PROCESS EACH ROW
        # ========================================================

        for row in rows:

            row_result = dict(row)

            validation_errors = []

            # ----------------------------------------------------
            # VALIDATE ROW FIELDS
            # ----------------------------------------------------

            for field_name, rules in validation_set.items():

                value = row.get(
                    field_name
                )

                # -----------------------------------------------
                # REQUIRED FIELD CHECK
                # -----------------------------------------------

                if field_name in import_required_fields:

                    if (
                        value is None
                        or (
                            isinstance(value, str)
                            and not value.strip()
                        )
                    ):

                        validation_errors.append(
                            f"{field_name} is required."
                        )

                        continue

                # -----------------------------------------------
                # OPTIONAL FIELD EMPTY → IGNORE
                # -----------------------------------------------

                if (
                    value is None
                    or (
                        isinstance(value, str)
                        and not value.strip()
                    )
                ):

                    continue

                # -----------------------------------------------
                # STRING TRIMMING
                # -----------------------------------------------

                if isinstance(value, str):

                    value = value.strip()

                    row[field_name] = value

                # -----------------------------------------------
                # LENGTH VALIDATION
                # -----------------------------------------------

                length_rule = rules.get(
                    "length"
                )

                if length_rule:

                    min_length = length_rule.get(
                        "min"
                    )

                    max_length = length_rule.get(
                        "max"
                    )

                    if isinstance(value, str):

                        value_length = len(value)

                        if (
                            min_length is not None
                            and value_length < min_length
                        ):

                            validation_errors.append(
                                f"{field_name} must be "
                                f"at least {min_length} "
                                "characters."
                            )

                        elif (
                            max_length is not None
                            and value_length > max_length
                        ):

                            validation_errors.append(
                                f"{field_name} must not exceed "
                                f"{max_length} characters."
                            )

                # -----------------------------------------------
                # ENUM VALIDATION
                # -----------------------------------------------

                enum_helper = rules.get(
                    "enum"
                )

                if enum_helper:

                    is_valid = enum_helper[
                        "validate"
                    ](value)

                    if not is_valid:

                        valid_values = enum_helper[
                            "get_valid_values"
                        ]()

                        validation_errors.append(
                            f"{field_name} has an invalid "
                            f"value '{value}'. "
                            f"Allowed values: "
                            f"{', '.join(valid_values)}"
                        )

            # ====================================================
            # INVALID ROW
            # ====================================================

            if validation_errors:

                row_result["isValid"] = False

                row_result["invalidReason"] = (
                    "; ".join(validation_errors)
                )

                row_result["modelOutput"] = (
                    "Not Applicable"
                )

                invalid_rows_count += 1

                processed_rows.append(
                    row_result
                )

                continue

            # ====================================================
            # VALID ROW → CLASSIFICATION MODEL
            # ====================================================

            try:

                model_output = classify_entity(
                    row.get("projectTitle"),
                    row.get("projectDescription"),
                    row.get("problemStatement"),
                    row.get("projectGoal"),
                    row.get("projectType"),
                    row.get("productVision"),
                    row.get("entityTitle"),
                    row.get("entityDescription"),
                    entity_model
                )

                row_result["isValid"] = True

                row_result["invalidReason"] = (
                    "Not Applicable"
                )

                row_result["modelOutput"] = (
                    model_output
                )

                valid_rows_count += 1

            except Exception as error:

                row_result["isValid"] = False

                row_result["invalidReason"] = (
                    "Entity classification failed."
                )

                row_result["modelOutput"] = (
                    "Not Applicable"
                )

                invalid_rows_count += 1

                log_with_time(
                    f"❌ Entity classification failed "
                    f"for rowId={row.get('rowId')}: "
                    f"{str(error)}"
                )

            processed_rows.append(
                row_result
            )

        # ========================================================
        # FINAL RESULT
        # ========================================================

        result = {

            "totalRows": len(rows),

            "validRows": valid_rows_count,

            "invalidRows": invalid_rows_count,

            "rows": processed_rows
        }

        log_with_time(
            "✅ [import_entity_type_controller] "
            f"Processed {len(rows)} rows | "
            f"Valid: {valid_rows_count} | "
            f"Invalid: {invalid_rows_count}"
        )

        return entity_type_bulk_import_success(
            result
        )

    except Exception as error:

        log_with_time(
            "❌ [import_entity_type_controller] "
            "Unexpected error while processing entity type import."
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )