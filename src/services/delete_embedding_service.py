from sqlalchemy.orm import Session

from src.models.embedding import Embedding


def delete_embedding_service(
    db: Session,
    entity_id,
    entity_type
):
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

    db.delete(existing_embedding)
    db.commit()

    return True