# middlewares/llm/field_validation_middleware.py

from src.configs.validation_sets import validation_sets
from src.middlewares.factory.field_validation_middleware_factory import validate_body


validation_middlewares = {

    "convert_content_to_english_validation_middleware":
        validate_body(
            "convertContentToEnglish",
            validation_sets["convert_content_to_english_validation_set"]
        )

}