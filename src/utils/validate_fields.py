def validate_missing_fields(data, required_fields):
    """
    Generic utility to check for missing fields and trim string values.

    :param data: req.body, req.query, or req.params
    :param required_fields: ["email", "password", "userId"]
    """

    missing_fields = []

    # Original data ko mutate na karne ke liye copy
    cleaned_data = dict(data)

    for field in required_fields:
        value = cleaned_data.get(field)

        # 1. Check if field is missing
        # JS: undefined, null, or empty/whitespace string
        if (
            value is None
            or (isinstance(value, str) and value.strip() == "")
        ):
            missing_fields.append(field)

        else:
            # 2. Agar string hai toh trim kar do
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

    return {
        "isValid": len(missing_fields) == 0,
        "missingFields": missing_fields,
        "cleanedData": cleaned_data
    }


def validate_required_columns(
    headers=None,
    required_columns=None,
    options=None
):

    if headers is None:
        headers = []

    if required_columns is None:
        required_columns = []

    if options is None:
        options = {}

    ignore_case = options.get(
        "ignoreCase",
        True
    )

    trim = options.get(
        "trim",
        True
    )

    # ============================================================
    # NORMALIZE
    # ============================================================

    def normalize(value):

        value = str(value)

        if trim:
            value = value.strip()

        if ignore_case:
            value = value.lower()

        return value

    # ============================================================
    # NORMALIZED HEADERS
    # ============================================================

    normalized_headers = [
        normalize(header)
        for header in headers
    ]

    # ============================================================
    # HEADER SET
    # ============================================================

    header_set = set(
        normalized_headers
    )

    # ============================================================
    # MISSING COLUMNS
    # ============================================================

    missing_columns = [
        column
        for column in required_columns
        if normalize(column) not in header_set
    ]

    # ============================================================
    # DUPLICATE COLUMNS
    # ============================================================

    duplicate_columns = list(
        dict.fromkeys(
            header
            for index, header
            in enumerate(normalized_headers)
            if normalized_headers.index(header) != index
        )
    )

    # ============================================================
    # RESULT
    # ============================================================

    return {
        "isValid": (
            len(missing_columns) == 0
            and len(duplicate_columns) == 0
        ),

        "missingColumns": missing_columns,

        "duplicateColumns": duplicate_columns,

        "cleanedHeaders": headers
    }