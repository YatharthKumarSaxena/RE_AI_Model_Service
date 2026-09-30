import csv
from collections import Counter

INPUT_CSV = "entity_classifier_data.csv"

EXPECTED_COLUMNS = [
    "rowId",
    "projectTitle",
    "projectDescription",
    "problemStatement",
    "projectGoal",
    "projectType",
    "productVision",
    "entityTitle",
    "entityDescription",
    "entityType",
]

VALID_PROJECT_TYPES = {
    "development",
    "enhancement",
    "maintenance",
}

VALID_ENTITY_TYPES = {
    "REQUIREMENT",
    "HIGH_LEVEL_FEATURE",
    "CONSTRAINT",
    "EXTERNAL_INTERFACE",
    "SCOPE",
    "INVALID_IRRELEVANT",
}


def main():

    print("=" * 70)
    print("ENTITY CLASSIFIER DATASET AUDIT")
    print("=" * 70)

    total_rows = 0
    valid_rows = 0

    class_counts = Counter()
    project_type_counts = Counter()

    duplicate_signatures = Counter()
    duplicate_rows = {}
    duplicate_row_ids = []

    malformed_rows = []
    missing_required = []
    invalid_project_types = []
    invalid_entity_types = []
    invalid_row_ids = []

    required_fields = [
        "projectTitle",
        "projectDescription",
        "problemStatement",
        "projectGoal",
        "projectType",
        "entityTitle",
    ]

    with open(
        INPUT_CSV,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.reader(file)

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        header = next(reader, None)

        if header is None:
            print("ERROR: CSV is empty.")
            return

        print("\n[1] HEADER CHECK")

        if header == EXPECTED_COLUMNS:
            print("PASS: Header is correct.")
        else:
            print("FAIL: Header mismatch")
            print("\nExpected:")
            print(EXPECTED_COLUMNS)
            print("\nFound:")
            print(header)

        # --------------------------------------------------
        # ROW CHECK
        # --------------------------------------------------

        for line_number, row in enumerate(reader, start=2):

            total_rows += 1

            # --------------------------------------------------
            # COLUMN COUNT
            # --------------------------------------------------

            if len(row) != len(EXPECTED_COLUMNS):

                malformed_rows.append(
                    {
                        "line": line_number,
                        "columns": len(row),
                        "expected": len(EXPECTED_COLUMNS),
                        "row": row,
                    }
                )

                continue

            data = dict(zip(EXPECTED_COLUMNS, row))

            # --------------------------------------------------
            # ROW ID
            # --------------------------------------------------

            try:
                row_id = int(data["rowId"])

                if row_id <= 0:
                    invalid_row_ids.append(
                        (line_number, data["rowId"])
                    )

            except ValueError:
                invalid_row_ids.append(
                    (line_number, data["rowId"])
                )

            # --------------------------------------------------
            # REQUIRED FIELDS
            # --------------------------------------------------

            empty_fields = []

            for field in required_fields:

                if not data[field].strip():
                    empty_fields.append(field)

            if empty_fields:

                missing_required.append(
                    {
                        "line": line_number,
                        "rowId": data["rowId"],
                        "fields": empty_fields,
                    }
                )

            # --------------------------------------------------
            # PROJECT TYPE
            # --------------------------------------------------

            project_type = data["projectType"].strip()

            project_type_counts[project_type] += 1

            if project_type not in VALID_PROJECT_TYPES:

                invalid_project_types.append(
                    {
                        "line": line_number,
                        "rowId": data["rowId"],
                        "value": project_type,
                    }
                )

            # --------------------------------------------------
            # ENTITY TYPE
            # --------------------------------------------------

            entity_type = data["entityType"].strip()

            class_counts[entity_type] += 1

            if entity_type not in VALID_ENTITY_TYPES:

                invalid_entity_types.append(
                    {
                        "line": line_number,
                        "rowId": data["rowId"],
                        "value": entity_type,
                    }
                )

            # --------------------------------------------------
            # EXACT DUPLICATE SIGNATURE
            # Exclude rowId because duplicate content
            # with different IDs is still a duplicate.
            # --------------------------------------------------

            signature = tuple(
                data[column].strip().lower()
                for column in EXPECTED_COLUMNS
                if column != "rowId"
            )

            duplicate_signatures[signature] += 1

            if signature not in duplicate_rows:
                duplicate_rows[signature] = []

            duplicate_rows[signature].append({
                "line": line_number,
                "rowId": data["rowId"]
            })

            valid_rows += 1

    # ==========================================================
    # RESULTS
    # ==========================================================

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)

    print(f"\nTotal data rows          : {total_rows}")
    print(f"Structurally valid rows : {valid_rows}")
    print(f"Malformed rows           : {len(malformed_rows)}")

    # ----------------------------------------------------------
    # CLASS DISTRIBUTION
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("ENTITY TYPE DISTRIBUTION")
    print("-" * 70)

    for entity_type in sorted(VALID_ENTITY_TYPES):

        count = class_counts[entity_type]

        percentage = (
            count / total_rows * 100
            if total_rows
            else 0
        )

        print(
            f"{entity_type:22} : "
            f"{count:4} ({percentage:6.2f}%)"
        )

    # ----------------------------------------------------------
    # PROJECT TYPE
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("PROJECT TYPE DISTRIBUTION")
    print("-" * 70)

    for project_type, count in project_type_counts.items():

        print(
            f"{project_type:15} : {count}"
        )

    # ----------------------------------------------------------
    # MALFORMED
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("MALFORMED ROWS")
    print("-" * 70)

    if not malformed_rows:

        print("PASS: No malformed rows.")

    else:

        print(
            f"FAIL: {len(malformed_rows)} malformed rows found."
        )

        for item in malformed_rows[:50]:

            print(
                f"Line {item['line']} | "
                f"Columns={item['columns']} | "
                f"Expected={item['expected']}"
            )

    # ----------------------------------------------------------
    # MISSING REQUIRED
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("MISSING REQUIRED FIELDS")
    print("-" * 70)

    if not missing_required:

        print("PASS: No missing required fields.")

    else:

        print(
            f"FAIL: {len(missing_required)} rows have "
            f"missing required fields."
        )

        for item in missing_required[:50]:

            print(
                f"Line {item['line']} | "
                f"rowId={item['rowId']} | "
                f"Missing={item['fields']}"
            )

    # ----------------------------------------------------------
    # INVALID PROJECT TYPE
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("INVALID PROJECT TYPES")
    print("-" * 70)

    if not invalid_project_types:

        print("PASS: All projectType values are valid.")

    else:

        print(
            f"FAIL: {len(invalid_project_types)} invalid values."
        )

        for item in invalid_project_types[:50]:

            print(
                f"Line {item['line']} | "
                f"rowId={item['rowId']} | "
                f"value='{item['value']}'"
            )

    # ----------------------------------------------------------
    # INVALID ENTITY TYPE
    # ----------------------------------------------------------

    print("\n" + "-" * 70)
    print("INVALID ENTITY TYPES")
    print("-" * 70)

    if not invalid_entity_types:

        print("PASS: All entityType values are valid.")

    else:

        print(
            f"FAIL: {len(invalid_entity_types)} invalid values."
        )

        for item in invalid_entity_types[:50]:

            print(
                f"Line {item['line']} | "
                f"rowId={item['rowId']} | "
                f"value='{item['value']}'"
            )

    # ----------------------------------------------------------
    # DUPLICATES
    # ----------------------------------------------------------

    duplicate_groups = [
        signature
        for signature, count in duplicate_signatures.items()
        if count > 1
    ]

    if duplicate_groups:
        print(f"FAIL: {len(duplicate_groups)} duplicate groups found.")

        for signature in duplicate_groups:
            print("\nDuplicate group:")

            for row in duplicate_rows[signature]:
                print(
                    f"Line {row['line']} | "
                    f"rowId={row['rowId']}"
                )

    if not duplicate_groups:

        print("PASS: No exact duplicate rows.")

    else:

        print(
            f"FAIL: {len(duplicate_groups)} duplicate groups found."
        )

    # ----------------------------------------------------------
    # FINAL STATUS
    # ----------------------------------------------------------

    has_errors = (
        len(malformed_rows) > 0
        or len(missing_required) > 0
        or len(invalid_project_types) > 0
        or len(invalid_entity_types) > 0
        or len(invalid_row_ids) > 0
        or len(duplicate_groups) > 0
    )

    print("\n" + "=" * 70)

    if has_errors:
        print("AUDIT STATUS: FAIL")
        print("Dataset ko training se pehle clean karna hoga.")
    else:
        print("AUDIT STATUS: PASS")
        print("Dataset structurally ready for next stage.")

    print("=" * 70)


if __name__ == "__main__":
    main()