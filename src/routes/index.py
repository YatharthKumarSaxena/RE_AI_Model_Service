from src.configs.uris import (
    LLM_BASE,
    CLASSIFICATION_BASE,
    DATA_INSIGHT_BASE,
    EVALUATION_BASE
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


def register_routes(app):

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