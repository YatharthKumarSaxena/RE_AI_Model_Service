from src.middlewares.factory.parse_file_middleware_factory import (
    create_parse_file_middleware
)

from src.utils.spreadsheet_parser import (
    spreadsheet_parser
)


parse_file_middlewares = {
    "parse_entity_type_spreadsheet_file_middleware":
        create_parse_file_middleware(
            middleware_name="Entity Type Spreadsheet Parser",
            parsers=[
                spreadsheet_parser
            ]
        )
}