from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.embedding import Embedding

from ml.models.detect_duplicate.embedding_model import (
    embedding_model
)

from src.configs.threshold import (
    THRESHOLD
)


DUPLICATE_THRESHOLD = THRESHOLD["duplicate_detection"]["duplicate"]
REVIEW_THRESHOLD = THRESHOLD["duplicate_detection"]["review"]


def check_duplicate_service(
    db: Session,
    project_id,
    entity_id,
    entity_type,
    title,
    description
):

    if not title and not description:

        raise ValueError(
            "Title or description is required"
        )

    content = (
        f"{title}\n{description}"
    ).strip()

    new_embedding = (
        embedding_model.generate_embedding(
            content
        )
    )

    stmt = select(
        Embedding
    ).where(
        Embedding.project_id == project_id,
        Embedding.entity_type == entity_type,
        Embedding.entity_id != entity_id
    )

    existing_embeddings = (
        db.execute(stmt)
        .scalars()
        .all()
    )

    if not existing_embeddings:

        return {
            "result": "UNIQUE",
            "matches": []
        }

    matches = []

    for existing in existing_embeddings:

        score = cosine_similarity(
            new_embedding,
            existing.embedding
        )

        if score >= DUPLICATE_THRESHOLD:

            result = "DUPLICATE"

        elif score >= REVIEW_THRESHOLD:

            result = "REVIEW"

        else:

            continue

        matches.append({
            "entity_id": existing.entity_id,
            "confidence_score": round(
                score,
                4
            ),
            "result": result
        })

    matches.sort(
        key=lambda item: item[
            "confidence_score"
        ],
        reverse=True
    )

    if not matches:

        overall_result = "UNIQUE"

    elif any(
        match["result"] == "DUPLICATE"
        for match in matches
    ):

        overall_result = "DUPLICATE"

    else:

        overall_result = "REVIEW"

    return {
        "result": overall_result,
        "matches": matches
    }


def cosine_similarity(
    vector_a,
    vector_b
):

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b
        )
    )

    magnitude_a = sum(
        a * a
        for a in vector_a
    ) ** 0.5

    magnitude_b = sum(
        b * b
        for b in vector_b
    ) ** 0.5

    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )