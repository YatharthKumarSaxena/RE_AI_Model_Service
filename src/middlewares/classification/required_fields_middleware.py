# middlewares/classification/required_fields_middleware.py

from src.middlewares.factory.required_fields_middleware_factory import check_body_presence
from src.configs.required_fields import required_fields

required_fields_middlewares = {
    "classify_entity_type_required_fields_middleware": check_body_presence(
        "classifyEntityTypePresence", 
        required_fields["classify_entity_type_field"]
    )
}