import os
import csv

from src.utils.project_path import (
    PROJECT_ROOT
)

from src.responses.success.data_insight import (
    dataset_success
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


def get_dataset_controller():

    try:

        csv_path = os.path.join(
            PROJECT_ROOT,
            "ml",
            "data",
            "entity_classifier_data.csv"
        )

        rows = []

        with open(
            csv_path,
            mode="r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(
                file
            )

            for row in reader:

                rows.append(
                    row
                )

        log_with_time(
            "✅ [get_dataset_controller] "
            f"Dataset loaded successfully: "
            f"{len(rows)} rows"
        )

        return dataset_success(
            rows
        )

    except Exception as error:

        log_with_time(
            "❌ [get_dataset_controller] "
            "Failed to load dataset"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )