import os
import csv
from collections import Counter

from src.utils.project_path import (
    PROJECT_ROOT
)

from src.responses.success.data_insight import (
    dataset_insights_success
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


def get_dataset_insights_controller():

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

                rows.append(row)

        total_records = len(rows)

        if total_records == 0:

            return dataset_insights_success({
                "totalRecords": 0,
                "uniqueProjects": 0,
                "totalEntityTypes": 0,
                "entityDistribution": {},
                "projectTypeDistribution": {},
                "averageRecordsPerProject": 0,
                "missingFields": {},
                "averageFieldLengths": {},
                "duplicateRows": 0,
                "uniqueEntityTitles": 0,
                "uniqueProjectTitles": 0
            })

        entity_distribution = Counter(
            row.get(
                "entityType",
                ""
            ).strip()
            for row in rows
            if row.get(
                "entityType",
                ""
            ).strip()
        )

        project_type_distribution = Counter(
            row.get(
                "projectType",
                ""
            ).strip()
            for row in rows
            if row.get(
                "projectType",
                ""
            ).strip()
        )

        unique_projects = set(
            row.get(
                "projectTitle",
                ""
            ).strip()
            for row in rows
            if row.get(
                "projectTitle",
                ""
            ).strip()
        )

        unique_project_titles = len(
            unique_projects
        )

        unique_entity_titles = len(
            set(
                row.get(
                    "entityTitle",
                    ""
                ).strip()
                for row in rows
                if row.get(
                    "entityTitle",
                    ""
                ).strip()
            )
        )

        average_records_per_project = (
            round(
                total_records /
                unique_project_titles,
                2
            )
            if unique_project_titles
            else 0
        )

        fields = [
            "projectTitle",
            "projectDescription",
            "problemStatement",
            "projectGoal",
            "projectType",
            "productVision",
            "entityTitle",
            "entityDescription",
            "entityType"
        ]

        missing_fields = {}
        average_field_lengths = {}

        for field in fields:

            missing_count = 0
            total_length = 0
            non_empty_count = 0

            for row in rows:

                value = (
                    row.get(
                        field,
                        ""
                    )
                    or ""
                ).strip()

                if not value:

                    missing_count += 1

                    continue

                total_length += len(value)
                non_empty_count += 1

            missing_fields[field] = (
                missing_count
            )

            average_field_lengths[field] = (
                round(
                    total_length /
                    non_empty_count,
                    2
                )
                if non_empty_count
                else 0
            )

        row_signatures = [
            tuple(
                row.get(
                    field,
                    ""
                )
                for field in fields
            )
            for row in rows
        ]

        duplicate_rows = (
            total_records -
            len(
                set(row_signatures)
            )
        )

        insights = {
            "totalRecords": total_records,
            "uniqueProjects":
                unique_project_titles,
            "totalEntityTypes":
                len(entity_distribution),
            "entityDistribution":
                dict(entity_distribution),
            "projectTypeDistribution":
                dict(
                    project_type_distribution
                ),
            "averageRecordsPerProject":
                average_records_per_project,
            "missingFields":
                missing_fields,
            "averageFieldLengths":
                average_field_lengths,
            "duplicateRows":
                duplicate_rows,
            "uniqueEntityTitles":
                unique_entity_titles,
            "uniqueProjectTitles":
                unique_project_titles
        }

        log_with_time(
            "✅ [get_dataset_insights_controller] "
            f"Dataset insights generated successfully | "
            f"Records: {total_records} | "
            f"Projects: {unique_project_titles} | "
            f"Entity Types: "
            f"{len(entity_distribution)}"
        )

        return dataset_insights_success(
            insights
        )

    except Exception as error:

        log_with_time(
            "❌ [get_dataset_insights_controller] "
            "Failed to generate dataset insights"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )