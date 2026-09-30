# configs/uris.py

BASE_PATH = "/re-model-service"
API_VERSION = "/api/v1"

API_PREFIX = f"{BASE_PATH}{API_VERSION}"

LLM_BASE = f"{API_PREFIX}/llm"
CLASSIFICATION_BASE = f"{API_PREFIX}/classification"
DATA_INSIGHT_BASE = f"{API_PREFIX}/data-insight"
EVALUATION_BASE = f"{API_PREFIX}/evaluation"

DATA_INSIGHT_ROUTES = {
    "DATASET": "/dataset",
    "DATASET_INSIGHTS": "/dataset-insights"
}

EVALUATION_ROUTES = {
    "MODEL_EVALUATION": "/model-evaluation"
}

LLM_ROUTES = {
    "CONVERT_CONTENT_TO_ENGLISH": "/convert-content-to-english"
}

CLASSIFICATION_ROUTES = {
    "CLASSIFY_ENTITY": "/classify-entity",
    "BULK_ENTITY_CLASSIFY": "/classify-bulk-entity"
}