import os
import csv

from src.utils.project_path import (
    PROJECT_ROOT
)

from src.responses.success.evaluation import (
    model_evaluation_success
)

from src.responses.common.error_handler import (
    throw_internal_server_error
)

from src.utils.time_stamps import (
    log_with_time
)

from src.utils.log_error import (
    error_message
)


def get_model_evaluation_controller():

    try:

        evaluation_dir = os.path.join(
            PROJECT_ROOT,
            "ml",
            "evaluation",
            "entityType"
        )

        evaluation_data = {}

        for filename in os.listdir(
            evaluation_dir
        ):

            if not filename.endswith(
                ".csv"
            ):
                continue

            file_path = os.path.join(
                evaluation_dir,
                filename
            )

            rows = []

            with open(
                file_path,
                mode="r",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(
                    file
                )

                for row in reader:

                    rows.append(row)

            file_key = os.path.splitext(
                filename
            )[0]

            evaluation_data[file_key] = rows

        log_with_time(
            "✅ [get_model_evaluation_controller] "
            "Model evaluation data loaded successfully | "
            f"Files: {len(evaluation_data)}"
        )

        return model_evaluation_success(
            evaluation_data
        )

    except Exception as error:

        log_with_time(
            "❌ [get_model_evaluation_controller] "
            "Failed to load model evaluation data"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )