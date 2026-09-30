import os
import joblib

from src.utils.take_output_from_model import (
    get_model_prediction
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "entityType"
)


# ============================================================
# TF-IDF
# ============================================================

TFIDF_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "entity_tfidf.joblib"
)

tfidf_vectorizer = joblib.load(
    TFIDF_MODEL_PATH
)


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATHS = {
    "linear_svm": os.path.join(
        MODEL_DIR,
        "entity_linear_svm.joblib"
    ),

    "sgd_classifier": os.path.join(
        MODEL_DIR,
        "entity_sgd_classifier.joblib"
    ),

    "ridge_classifier": os.path.join(
        MODEL_DIR,
        "entity_ridge_classifier.joblib"
    ),

    "logistic_regression": os.path.join(
        MODEL_DIR,
        "entity_logistic_regression.joblib"
    ),

    "complement_naive_bayes": os.path.join(
        MODEL_DIR,
        "entity_complement_naive_bayes.joblib"
    ),

    "bernoulli_naive_bayes": os.path.join(
        MODEL_DIR,
        "entity_bernoulli_naive_bayes.joblib"
    ),

    "multinomial_naive_bayes": os.path.join(
        MODEL_DIR,
        "entity_multinomial_naive_bayes.joblib"
    ),

    "extra_trees": os.path.join(
        MODEL_DIR,
        "entity_extra_trees.joblib"
    ),

    "random_forest": os.path.join(
        MODEL_DIR,
        "entity_random_forest.joblib"
    ),

    "decision_tree": os.path.join(
        MODEL_DIR,
        "entity_decision_tree.joblib"
    )
}


# ============================================================
# LOAD MODELS
# ============================================================

models = {
    model_name: joblib.load(model_path)
    for model_name, model_path in MODEL_PATHS.items()
}

# ============================================================
# ENTITY CLASSIFICATION
# ============================================================

def classify_entity(
    project_title: str,
    project_description: str,
    problem_statement: str,
    project_goal: str,
    project_type: str,
    product_vision: str,
    entity_title: str,
    entity_description: str,
    model_name: str
):

    project_title = project_title or ""
    project_description = project_description or ""
    problem_statement = problem_statement or ""
    project_goal = project_goal or ""
    project_type = project_type or ""
    product_vision = product_vision or ""
    entity_title = entity_title or ""
    entity_description = entity_description or ""

    # ========================================================
    # BUILD MODEL INPUT
    # ========================================================

    model_text = " ".join([
        project_title,
        project_description,
        problem_statement,
        project_goal,
        project_type,
        product_vision,
        entity_title,
        entity_description
    ])

    # ========================================================
    # TF-IDF
    # ========================================================

    text_vector = tfidf_vectorizer.transform(
        [model_text]
    )

    # ========================================================
    # GET MODEL
    # ========================================================

    model = models.get(
        model_name
    )

    if model is None:
        raise ValueError(
            f"Classification model not found: {model_name}"
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    return get_model_prediction(
        model,
        text_vector
    )