from sqlalchemy.orm import Session

from src.models.embedding import Embedding
from ml.models.detect_duplicate.embedding_model import embedding_model


def save_embedding_service(
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

    content = f"{title}\n{description}".strip()

    # Generate embedding
    vector = embedding_model.generate_embedding(
        content
    )

    # Check if embedding already exists
    existing_embedding = (
        db.query(Embedding)
        .filter(
            Embedding.entity_id == entity_id,
            Embedding.entity_type == entity_type
        )
        .first()
    )

    if existing_embedding:

        # Update existing embedding
        existing_embedding.project_id = project_id
        existing_embedding.content = content
        existing_embedding.embedding = vector

        db.commit()
        db.refresh(existing_embedding)

        return existing_embedding

    # Create new embedding
    new_embedding = Embedding(
        entity_id=entity_id,
        project_id=project_id,
        entity_type=entity_type,
        content=content,
        embedding=vector
    )

    db.add(new_embedding)
    db.commit()
    db.refresh(new_embedding)

    return new_embedding