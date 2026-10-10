from sqlalchemy.orm import Session

from src.models.embedding import Embedding

from ml.models.detect_duplicate.embedding_model import (
    embedding_model
)


def update_embedding_service(
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

    vector = (
        embedding_model.generate_embedding(
            content
        )
    )

    existing_embedding = (
        db.query(Embedding)
        .filter(
            Embedding.entity_id == entity_id,
            Embedding.entity_type == entity_type
        )
        .first()
    )

    if not existing_embedding:
        raise ValueError(
            "Embedding not found for entity"
        )

    existing_embedding.project_id = project_id
    existing_embedding.title = title
    existing_embedding.description = description
    existing_embedding.embedding = vector

    db.commit()
    db.refresh(existing_embedding)

    return existing_embedding