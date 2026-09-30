import re


# Checks if value exists in enum values
def is_valid_enum_value(enum_obj, value):
    return any(
        enum_value.value == value
        for enum_value in enum_obj
    )


# Checks if value exists in enum and returns boolean
def get_enum_key_by_value(enum_obj, value):
    return any(
        enum_value.value == value
        for enum_value in enum_obj
    )


# Validates string length
def validate_length(string, min_length, max_length):
    return min_length <= len(string) <= max_length


# Validates string against regex pattern
def is_valid_regex(string, regex):
    return bool(re.search(regex, string))


# Smart Error Message Generator for Length Validation
def generate_length_error_message(name, length, custom_message=None):
    if custom_message:
        return custom_message

    min_length = length.get("min")
    max_length = length.get("max")

    if min_length == max_length:
        return f"{name} must be exactly {min_length} characters"

    elif min_length and max_length:
        return (
            f"{name} must be between "
            f"{min_length} and {max_length} characters"
        )

    elif min_length:
        return f"{name} must be at least {min_length} characters"

    else:
        return f"{name} must not exceed {max_length} characters"