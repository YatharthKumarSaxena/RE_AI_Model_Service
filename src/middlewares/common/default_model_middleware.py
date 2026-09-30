from src.utils.enum_helpers import (
    EntityTypeModelHelper
)

from src.middlewares.factory.create_enum_default_middleware_factory import (
    create_enum_default_middleware
)

set_entity_model_middleware = create_enum_default_middleware(
    "setEntityModelMiddleware",
    EntityTypeModelHelper
)