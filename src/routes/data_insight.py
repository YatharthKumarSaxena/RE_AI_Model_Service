from flask import Blueprint

from src.configs.uris import (
    DATA_INSIGHT_BASE,
    DATA_INSIGHT_ROUTES
)

from src.middlewares.common.verify_device_field import (
    verify_device_field
)

from src.controllers.data_insight.get_entity_classify_data import (
    get_dataset_controller
)

from src.controllers.data_insight.get_entity_classify_insight import (
    get_dataset_insights_controller
)


data_insight_bp = Blueprint(
    "data_insight",
    __name__,
    url_prefix=DATA_INSIGHT_BASE
)


# ============================================================
# DATASET
# ============================================================

@data_insight_bp.route(
    DATA_INSIGHT_ROUTES["DATASET"],
    methods=["GET"]
)
def get_dataset():

    result = verify_device_field()

    if result is not None:
        return result

    return get_dataset_controller()


# ============================================================
# DATASET INSIGHTS
# ============================================================

@data_insight_bp.route(
    DATA_INSIGHT_ROUTES["DATASET_INSIGHTS"],
    methods=["GET"]
)
def get_dataset_insights():

    result = verify_device_field()

    if result is not None:
        return result

    return get_dataset_insights_controller()