from flask import jsonify

from src.configs.uris import (
    LLM_BASE,
    CLASSIFICATION_BASE,
    DATA_INSIGHT_BASE,
    EVALUATION_BASE,
    HEALTH_ROUTE
)

from src.routes.llm import (
    llm_router
)

from src.routes.classification import (
    classification_bp
)

from src.routes.data_insight import (
    data_insight_bp
)

from src.routes.evaluation import (
    evaluation_bp
)


def health_check():
    return jsonify({"status": "ok"})


def register_routes(app):

    app.add_url_rule(
        HEALTH_ROUTE,
        endpoint="health",
        view_func=health_check,
        methods=["GET"]
    )

    # LLM routes
    app.register_blueprint(
        llm_router,
        url_prefix=LLM_BASE
    )

    # Classification routes
    app.register_blueprint(
        classification_bp,
        url_prefix=CLASSIFICATION_BASE
    )

    # Data Insight routes
    app.register_blueprint(
        data_insight_bp,
        url_prefix=DATA_INSIGHT_BASE
    )

    # Evaluation routes
    app.register_blueprint(
        evaluation_bp,
        url_prefix=EVALUATION_BASE
    )