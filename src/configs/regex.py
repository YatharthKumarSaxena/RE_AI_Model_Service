# UUID v4
UUID_V4_REGEX = (
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"4[0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-"
    r"[0-9a-fA-F]{12}$"
)


# MongoDB ObjectId
MONGO_ID_REGEX = (
    r"^[0-9a-fA-F]{24}$"
)