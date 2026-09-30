# middlewares/classification/field_validation_middleware.py

from src.configs.validation_sets import validation_sets
from src.middlewares.factory.field_validation_middleware_factory import validate_body

validation_middlewares = {
    "classify_entity_type_validation_middleware": validate_body(
        "classifyEntityType",
        validation_sets["classify_entity_type_validation_set"]
    )
}