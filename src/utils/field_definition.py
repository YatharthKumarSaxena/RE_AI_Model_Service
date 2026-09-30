# utils/field_definition.py

def get_required_fields(definition):
    return [
        field_meta["field"]
        for field_meta in definition.values()
        if field_meta.get("required")
    ]


def get_validation_set(definition):
    return {
        field_meta["field"]: field_meta["validation"]
        for field_meta in definition.values()
        if field_meta.get("validation")
    }