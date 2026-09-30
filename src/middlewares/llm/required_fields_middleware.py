# middlewares/llm/required_fields_middleware.py

from src.middlewares.factory.required_fields_middleware_factory import check_body_presence
from src.configs.required_fields import required_fields


required_fields_middlewares = {

    "convert_content_to_english_required_fields_middleware":
        check_body_presence(
            "convertContentToEnglishPresence",
            required_fields["convert_content_to_english"]
        )

}